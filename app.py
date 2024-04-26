import numpy as np
from flask import Flask, render_template, Response, request, redirect, url_for
from ultralytics.utils.plotting import colors, Annotator

from tools.dir_tools import create_dir
from collections import defaultdict

import cv2
from sort import Sort
import datetime
from pytube import YouTube
from ultralytics import YOLO
from filterpy.kalman import KalmanFilter

app = Flask(__name__)

# Prepare CSV TODO change with true headers and create function to create and save (one function)
output_dir = create_dir("output")

# csv_manager_static = CSVManager(output_dir + "detected_persons_static.csv")
# csv_manager_frames = CSVManager(output_dir + "detected_persons_frames.csv")
# csv_manager_faces = CSVManager(output_dir + "detected_persons_faces.csv")

# header_static = ["UUID", "TrackID", "StartDate", "EndDate"]
# header_frames = ["UUID", "TrackID", "Class", "Confidence", "Coordinates", "Date"]
# header_faces = ["UUID", "Coordinates", "Date"]

# csv_manager_static.create_file_csv(header_static)
# csv_manager_frames.create_file_csv(header_frames)
# csv_manager_faces.create_file_csv(header_faces)

# Init Writers
# csv_manager_static.writer_file_csv()
# csv_manager_frames.writer_file_csv()
# csv_manager_faces.writer_file_csv()

# Init Models
model = YOLO('models/yolov8n.pt')
model_face = YOLO('models/yolov8n-face.pt')

# Other Params
cap = None
blur_ratio = 50
tracker = Sort()

track_history_persons = defaultdict(lambda: [])  # TODO SAVE TO CSV or DATABASE
track_history_persons_to_show = defaultdict(lambda: [])

data_frames_persons = defaultdict(lambda: [])  # TODO SAVE TO CSV or DATABASE
data_frames_faces = defaultdict(lambda: [])  # TODO SAVE TO CSV or DATABASE

detected_persons = {}
detected_history_persons = defaultdict(lambda: [])  # TODO SAVE TO CSV or DATABASE



# Inicialización del filtro de Kalman
kf = KalmanFilter(dim_x=4, dim_z=2)
kf.F = np.array([[1, 0, 1, 0],
                 [0, 1, 0, 1],
                 [0, 0, 1, 0],
                 [0, 0, 0, 1]])  # Matriz de transición
kf.H = np.array([[1, 0, 0, 0],
                 [0, 1, 0, 0]])  # Matriz de observación
kf.Q = np.eye(4) * 0.01  # Matriz de covarianza del proceso
kf.R = np.eye(2) * 1  # Matriz de covarianza del ruido de la medición
kf.x = np.zeros(4)  # Estado inicial
kf.P = np.eye(4)  # Covarianza inicial

# Función para predecir el estado futuro con el filtro de Kalman
def predict(kf):
    kf.predict()
    return kf.x[:2]

# Función para actualizar el estado del filtro de Kalman con una nueva detección
def update(kf, measurement):
    kf.update(measurement)
    return kf.x[:2]

def cap_start_video(type_video, video_url):
    global cap, track_history_persons, track_history_persons_to_show, detected_persons, data_frames_persons, data_frames_faces, detected_history_persons

    # TODO webcam url
    if type_video == "youtube":
        video = YouTube(video_url)
        stream = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        url = stream.url
    elif type_video == "stream":
        url = "http://elecam:$urfw3B!@wc1.marinavalencia.com/ISAPI/Streaming/channels/102/httpPreview"
    else:
        url = 0

    cap = cv2.VideoCapture(url)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    track_history_persons = defaultdict(lambda: [])
    track_history_persons_to_show = defaultdict(lambda: [])

    detected_persons = {}
    detected_history_persons = defaultdict(lambda: [])

    data_frames_persons = defaultdict(lambda: [])
    data_frames_faces = defaultdict(lambda: [])
    tracker = Sort()

    assert cap.isOpened(), "Error reading video file"


def cap_stop_video():
    global cap

    # TODO SAVE THERE CSV OR DATABASE

    if cap:
        cap.release()

    cv2.destroyAllWindows()
    # csv_manager_static.close_csv_file()
    # csv_manager_frames.close_csv_file()
    # csv_manager_faces.close_csv_file()


def get_time_on_screen(track_id):
    if track_id in detected_persons:
        time_on_screen = datetime.datetime.now() - detected_persons[track_id]
        hours, remainder = divmod(time_on_screen.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02}:{:02}:{:02}".format(hours, minutes, seconds)
    else:
        return "00:00:00"


def create_label(annotator, track_id, box, cls):
    label = "Person {} - Time: {}".format(str(track_id), get_time_on_screen(track_id))
    annotator.box_label(box, color=colors(int(cls), True), label=label)


def save_detected_person(track_id):
    if track_id not in detected_persons:
        detected_persons[track_id] = datetime.datetime.now()


def save_person_track_history(track_id, box):
    if track_id not in track_history_persons:
        track_history_persons[track_id] = []
        track_history_persons_to_show[track_id] = []

    track = track_history_persons[track_id]
    track_to_show = track_history_persons_to_show[track_id]

    track.append((int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)))
    track_to_show.append((int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)))

    if len(track) > 30:
        track_to_show.pop(0)

    return track_to_show


def show_person_track_history(frame, track, cls):
    points = np.array(track, dtype=np.int32).reshape((-1, 1, 2))
    cv2.circle(frame, (track[-1]), 7, colors(int(cls), True), -1)
    cv2.polylines(frame, [points], isClosed=False, color=colors(int(cls), True), thickness=2)


def check_person_visibility():
    for track_id, start_time in detected_persons.items():
        if track_id not in track_history_persons_to_show:
            end_time = datetime.datetime.now()
            detected_history_persons[track_id].append(
                [
                    start_time.timestamp(),
                    end_time.timestamp()
                ]
            )
            del detected_persons[track_id]


def finish_person_visibility():
    for track_id, start_time in detected_persons.items():
        end_time = datetime.datetime.now()
        detected_history_persons[track_id].append(
            [
                start_time.timestamp(),
                end_time.timestamp()
            ]
        )


def save_data_frames_persons(track_id, conf, box):
    if track_id not in data_frames_persons:
        data_frames_persons[track_id] = []

    data_frames_persons[track_id].append(
        [
            conf,
            box,
            datetime.datetime.now().timestamp()
        ]
    )


def detect_person_and_track(frame):
    results = model.track(frame, task='detect', persist=True, conf=0.6, verbose=False)

    for res in results:
        if res.boxes.id is not None:
            boxes = res.boxes.xyxy.cpu().numpy().astype(int)
            clss = res.boxes.cls.cpu().tolist()
            track_ids = res.boxes.id.int().cpu().tolist()
            confs = res.boxes.conf.cpu().tolist()

            tracks = tracker.update(boxes)
            tracks = tracks.astype(int)

            # for box, cls, track_id, conf in zip(boxes, clss, track_ids, confs):
            for (xmin, ymin, xmax, ymax, track_id), (cls, conf) in zip(tracks, zip(clss, confs)):
                if int(cls) == 0:
                    annotator = Annotator(frame, line_width=2)
                    create_label(annotator, track_id, [xmin, ymin, xmax, ymax], cls)

                    # Utilizar el filtro de Kalman para predecir la posición de la persona
                    prediction = predict(kf)
                    prediction = tuple(map(int, prediction))

                    # Dibujar la predicción en el fotograma
                    cv2.circle(frame, prediction, 5, (0, 255, 0), -1)

                    # Actualizar el estado del filtro de Kalman con la nueva detección
                    measurement = np.array(
                        [xmin, ymin])  # Utilizar la esquina superior izquierda del cuadro delimitador como medición
                    corrected_position = update(kf, measurement)

                    # Dibujar la posición corregida en el fotograma
                    cv2.circle(frame, tuple(map(int, corrected_position)), 5, (0, 0, 255), -1)

                    save_detected_person(track_id)

                    track = save_person_track_history(track_id, [xmin, ymin, xmax, ymax])
                    show_person_track_history(frame, track, cls)

                    save_data_frames_persons(track_id, conf, [xmin, ymin, xmax, ymax])

                    check_person_visibility()


def save_data_frames_faces(track_id, conf, box):
    face = data_frames_faces[track_id]
    face.append(
        [
            conf,
            box,
            datetime.datetime.now().timestamp()
        ]
    )


def detect_faces_and_blur(frame):
    results = model_face.track(frame, task='detect', conf=0.3, verbose=False)

    boxes = results[0].boxes.xyxy.cpu()
    confs = results[0].boxes.conf.cpu().tolist()

    for box, conf in zip(boxes, confs):
        face = frame[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
        blur_obj = cv2.blur(face, (blur_ratio, blur_ratio))

        frame[int(box[1]):int(box[3]), int(box[0]):int(box[2])] = blur_obj

        if results[0].boxes.id is not None:
            track_ids = results[0].boxes.id.int().cpu().tolist()
            for track_id in zip(track_ids):
                save_data_frames_faces(track_id, conf, box)


def generate_frames():
    global cap

    if cap:
        while cap.isOpened():
            success, frame = cap.read()

            if not success:
                print("No se ha podido leer el frame, Hemos llegado al final? Saliendo...")
                stop_video()
                break

            detect_faces_and_blur(frame)
            detect_person_and_track(frame)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def format_detected_persons():
    formatted_persons = []
    for key, value in detected_persons.items():
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


@app.route('/start_video', methods=['POST'])
def start_video():
    type = request.json['type']
    video_url = request.json['video_url']
    cap_start_video(type, video_url)
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
