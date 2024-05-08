import os
import numpy as np
from flask import Flask, render_template, Response, request, redirect, url_for
from ultralytics.utils.plotting import colors, Annotator

from collections import defaultdict

import cv2
from sort import Sort
import datetime
from pytube import YouTube
from ultralytics import YOLO
from dotenv import load_dotenv

import pika
import json
import streamlink

app = Flask(__name__)

load_dotenv()

# Init Models
model = YOLO('models/yolov8n.pt')
model_face = YOLO('models/yolov8n-face.pt')

# Other Params
cap = None
blur_ratio = 50
tracker = Sort()

# Array Params
track_history_persons_to_show = defaultdict(lambda: [])
detected_persons_to_show = defaultdict(lambda: [])


def send_data_to_queue(data, queue_name):
    try:
        credentials = pika.PlainCredentials(os.getenv("RABBIT_USER"), os.getenv("PASSWORD"))
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(os.getenv("RABBIT_HOST"), os.getenv("RABBIT_PORT"), credentials=credentials))
        channel = connection.channel()

        channel.queue_declare(queue=queue_name)
        channel.basic_publish(exchange='', routing_key=queue_name, body=data)

        connection.close()
    except Exception as e:
        print(f"Error al enviar datos a la cola {queue_name}:", e)


def cap_start_video():
    global cap, track_history_persons_to_show, detected_persons_to_show

    # LIVE YOUTUBE
    # live_video_url = os.getenv("VIDEO_LIVE")
    # streams = streamlink.streams(live_video_url)
    # url = streams["best"].url

    # VIDEO YOUTUBE
    video_url = os.getenv("VIDEO")
    video = YouTube(video_url)

    stream = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

    url = stream.url

    cap = cv2.VideoCapture(url)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    track_history_persons_to_show = defaultdict(lambda: [])
    detected_persons_to_show = defaultdict(lambda: [])

    tracker = Sort()

    assert cap.isOpened(), "Error reading video file"


def cap_stop_video():
    global cap

    finish_person_visibility()

    if cap:
        cap.release()

    cv2.destroyAllWindows()


def get_time_on_screen(track_id):
    if track_id in detected_persons_to_show:
        time_on_screen = datetime.datetime.now() - detected_persons_to_show[track_id]
        hours, remainder = divmod(time_on_screen.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02}:{:02}:{:02}".format(hours, minutes, seconds)
    else:
        return "00:00:00"


def create_label(annotator, track_id, box, cls):
    label = "Person {} - Time: {}".format(str(track_id), get_time_on_screen(track_id))
    annotator.box_label(box, color=colors(int(cls), True), label=label)


def save_detected_person(track_id):
    if track_id not in detected_persons_to_show:
        detected_persons_to_show[track_id] = datetime.datetime.now()


def save_track_history_database(track_id, conf, box):
    data = {
        "track_id": track_id.item(),
        "conf": conf,
        "cord_x": int((box[0] + box[2]) / 2),
        "cord_y": int((box[1] + box[3]) / 2)
    }

    data = json.dumps(data)

    send_data_to_queue(data, 'track_history')


def save_person_track_history(track_id, conf, box):
    if track_id not in track_history_persons_to_show:
        track_history_persons_to_show[track_id] = []

    track_to_show = track_history_persons_to_show[track_id]

    track_to_show.append((int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)))

    if len(track_to_show) > 30:
        track_to_show.pop(0)

    save_track_history_database(track_id, conf, box)

    return track_to_show


def show_person_track_history(frame, track, cls):
    points = np.array(track, dtype=np.int32).reshape((-1, 1, 2))
    cv2.circle(frame, (track[-1]), 7, colors(int(cls), True), -1)
    cv2.polylines(frame, [points], isClosed=False, color=colors(int(cls), True), thickness=2)


def save_person_database(track_id, start_time):
    end_time = datetime.datetime.now()

    data = {
        "track_id": track_id,
        "start_time": start_time.timestamp(),
        "end_time": end_time.timestamp()
    }
    send_data_to_queue(data, 'detected_persons')


def check_person_visibility():
    for track_id, start_time in detected_persons_to_show.items():
        if track_id not in track_history_persons_to_show:
            save_person_database(track_id, start_time)
            del detected_persons_to_show[track_id]


def finish_person_visibility():
    for track_id, start_time in detected_persons_to_show.items():
        save_person_database(track_id, start_time)


def calculate_velocity(track_id):
    track_history = track_history_persons_to_show.get(track_id, [])

    if len(track_history) < 2:
        return (0, 0)

    last_position = track_history[-1]
    second_last_position = track_history[-2]

    delta_x = last_position[0] - second_last_position[0]
    delta_y = last_position[1] - second_last_position[1]

    velocity_x = delta_x / 1
    velocity_y = delta_y / 1

    return (velocity_x, velocity_y)


def generate_predicted_track(point, estimated_velocity):
    x, y = point[0], point[1]

    predicted_track = []

    for i in range(10):
        predicted_x = x + estimated_velocity[0]
        predicted_y = y + estimated_velocity[1]
        predicted_track.append(
            (int(predicted_x), int(predicted_y)))

        x, y = predicted_x, predicted_y

    return predicted_track


def show_person_predicted_track(frame, predictions):
    predicted_points = np.array(predictions, dtype=np.int32).reshape((-1, 1, 2))
    cv2.polylines(frame, [predicted_points], isClosed=False, color=(0, 255, 0), thickness=2,
                  lineType=cv2.LINE_AA)
    cv2.circle(frame, predictions[-1], 7, (0, 255, 0), -1)


def detect_person_and_track(frame):
    results = model.track(frame, persist=True, conf=0.6, verbose=False)

    for res in results:
        if res.boxes.id is not None:
            boxes = res.boxes.xyxy.cpu().numpy().astype(int)
            clss = res.boxes.cls.cpu().tolist()
            confs = res.boxes.conf.cpu().tolist()

            tracks = tracker.update(boxes)
            tracks = tracks.astype(int)

            for (xmin, ymin, xmax, ymax, track_id), (cls, conf) in zip(tracks, zip(clss, confs)):
                if int(cls) == 0:
                    annotator = Annotator(frame, line_width=2)
                    create_label(annotator, track_id, [xmin, ymin, xmax, ymax], cls)

                    check_person_visibility()
                    save_detected_person(track_id)

                    # Track
                    track = save_person_track_history(track_id, conf, [xmin, ymin, xmax, ymax])
                    show_person_track_history(frame, track, cls)

                    # Predict Track
                    estimated_velocity = calculate_velocity(track_id)
                    point = track[-1]

                    predicted_track = generate_predicted_track(point, estimated_velocity)
                    show_person_predicted_track(frame, predicted_track)


def detect_faces_and_blur(frame):
    results = model_face.track(frame, task='detect', conf=0.3, verbose=False)

    boxes = results[0].boxes.xyxy.cpu()
    confs = results[0].boxes.conf.cpu().tolist()

    for box, conf in zip(boxes, confs):
        face = frame[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
        blur_obj = cv2.blur(face, (blur_ratio, blur_ratio))

        frame[int(box[1]):int(box[3]), int(box[0]):int(box[2])] = blur_obj


def generate_frames():
    global cap

    if cap:
        while cap.isOpened():
            success, frame = cap.read()

            if not success:
                print("Se terminaron los frames")
                finish_person_visibility()
                cap_stop_video()
                break

            detect_faces_and_blur(frame)
            detect_person_and_track(frame)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def format_detected_persons():
    formatted_persons = []
    for key, value in detected_persons_to_show.items():
        formatted_date = value.strftime("%H:%M:%S")
        formatted_person = f"Person {key} - Date: {formatted_date} <br>"
        formatted_persons.append(formatted_person)
    return formatted_persons


# FLASK ROUTES
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video', methods=['GET'])
def video():
    return render_template('video.html')


@app.route('/start_video', methods=['GET'])
def start_video():
    cap_start_video()
    return redirect(url_for('video'))


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/persons_feed')
def persons_feed():
    return Response(format_detected_persons())


@app.route('/stop_video')
def stop_video():
    cap_stop_video()

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
