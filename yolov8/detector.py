import asyncio
import json
import base64
import datetime
import os

import pika
from dotenv import load_dotenv
import cv2
import streamlink
import websockets
import numpy as np

from collections import defaultdict
from pytube import YouTube
import torch
from deep_sort_realtime.deepsort_tracker import DeepSort

from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors

load_dotenv()


class FaceDetector:
    def __init__(self, model_path, device):
        self.model = YOLO(model_path, task='detect').to(device)
        self.blur_ratio = 50

    def detect_faces(self, frame):
        results = self.model.track(frame, conf=0.2, verbose=False)

        for result in results:
            boxes = result.boxes.xyxy.cpu()

            for box in boxes:
                face = frame[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
                blur_obj = cv2.blur(face, (self.blur_ratio, self.blur_ratio))

                frame[int(box[1]):int(box[3]), int(box[0]):int(box[2])] = blur_obj


class PersonDetector:
    def __init__(self, model_path, device):
        self.model = YOLO(model_path).to(device)
        self.tracker = DeepSort(n_init=1, max_age=50)
        self.track_history_persons_to_show = defaultdict(lambda: [])
        self.detected_persons_to_show = defaultdict(lambda: [])
        self.setup_rabbitmq_connection()

    def setup_rabbitmq_connection(self):
        credentials = pika.PlainCredentials(os.getenv("RABBIT_USER"), os.getenv("RABBIT_PASSWORD"))
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(os.getenv("RABBIT_HOST"), os.getenv("RABBIT_PORT"), credentials=credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='detected_persons')
        self.channel.queue_declare(queue='track_history')

    def send_data_to_queue(self, data, queue_name):
        try:
            self.channel.basic_publish(exchange='', routing_key=queue_name, body=data)
        except Exception as e:
            print("Error al enviar datos a la cola:", e)

    def save_person_database(self, track_id, start_time):
        end_time = datetime.datetime.now()

        data = {
            "track_id": track_id,
            "start_time": start_time.timestamp(),
            "end_time": end_time.timestamp()
        }

        data = json.dumps(data)

        self.send_data_to_queue(data, 'detected_persons')

    def save_track_history_database(self, track):
        box = track.to_tlwh()

        data = {
            "track_id": track.track_id,
            "conf": track.det_conf,
            "cord_x": int((box[0] + box[2]) / 2),
            "cord_y": int((box[1] + box[3]) / 2),
            "mean": track.mean.tolist(),
            "covariance": track.covariance.tolist(),
            "hits": track.hits,
            "age": track.age,
            "time_since_update": track.time_since_update,
            "state": track.state,
            "time": datetime.datetime.now().timestamp()
        }

        data = json.dumps(data)

        self.send_data_to_queue(data, 'track_history')

    def create_label(self, annotator, track):
        label = "Person {}".format(str(track.track_id))
        annotator.box_label(track.to_tlwh(), color=colors(int(0), True), label=label)

    def save_detected_person(self, track_id):
        if track_id not in self.detected_persons_to_show:
            self.detected_persons_to_show[track_id] = datetime.datetime.now()

    def get_time_on_screen(self, track_id):
        if track_id in self.detected_persons_to_show:
            time_on_screen = datetime.datetime.now() - self.detected_persons_to_show[track_id]
            hours, remainder = divmod(time_on_screen.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return "{:02}:{:02}:{:02}".format(hours, minutes, seconds)
        else:
            return "00:00:00"

    def format_detected_persons(self):
        formatted_persons = []
        for track in self.tracker.tracker.tracks:
            formatted_date = self.get_time_on_screen(track.track_id)
            formatted_person = f"Person {track.track_id} - Time: {formatted_date} </br>"
            formatted_persons.append(formatted_person)
        return formatted_persons

    def save_person_track_history(self, track):
        box = track.to_tlwh()

        if track.track_id not in self.track_history_persons_to_show:
            self.track_history_persons_to_show[track.track_id] = []

        track_to_show = self.track_history_persons_to_show[track.track_id]

        track_to_show.append((int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)))

        if len(track_to_show) > 30:
            track_to_show.pop(0)

        return track_to_show

    def show_person_track_history(self, frame, track_to_show):
        points = np.array(track_to_show, dtype=np.int32).reshape((-1, 1, 2))
        cv2.circle(frame, (track_to_show[-1]), 7, colors(int(0), True), -1)
        cv2.polylines(frame, [points], isClosed=False, color=colors(int(0), True), thickness=2)

    def calculate_velocity(self, track_id):
        track_history = self.track_history_persons_to_show.get(track_id, [])

        if len(track_history) < 2:
            return (0, 0)

        last_position = track_history[-1]
        second_last_position = track_history[-2]

        delta_x = last_position[0] - second_last_position[0]
        delta_y = last_position[1] - second_last_position[1]

        velocity_x = delta_x / 1
        velocity_y = delta_y / 1

        return (velocity_x, velocity_y)

    def generate_predicted_track(self, point, estimated_velocity):
        x, y = point[0], point[1]

        predicted_track = []

        for i in range(10):
            predicted_x = x + estimated_velocity[0]
            predicted_y = y + estimated_velocity[1]
            predicted_track.append(
                (int(predicted_x), int(predicted_y)))

            x, y = predicted_x, predicted_y

        return predicted_track

    def show_person_predicted_track(self, frame, predictions):
        predicted_points = np.array(predictions, dtype=np.int32).reshape((-1, 1, 2))
        cv2.polylines(frame, [predicted_points], isClosed=False, color=(0, 255, 0), thickness=2,
                      lineType=cv2.LINE_AA)
        cv2.circle(frame, predictions[-1], 7, (0, 255, 0), -1)

    def check_person_visibility(self):
        tracked_ids = list(self.detected_persons_to_show.keys())

        for track_id in tracked_ids:
            track_found = False
            for track in self.tracker.tracker.tracks:
                if track.track_id == track_id:
                    track_found = True
                    break

            if not track_found:
                self.save_person_database(track_id, self.detected_persons_to_show[track_id])
                del self.detected_persons_to_show[track_id]

    def finish_person_visibility(self):
        for track_id, start_time in self.detected_persons_to_show.items():
            self.save_person_database(track_id, start_time)

    def detect_persons(self, frame):
        results = self.model.track(frame, persist=True, conf=0.5, verbose=False)

        for res in results:
            if res.boxes.id is not None:
                boxes = res.boxes.xyxy.cpu().numpy().astype(int)
                clss = res.boxes.cls.cpu().tolist()
                confs = res.boxes.conf.cpu().tolist()

                detections = [(boxes[i], confs[i], clss[i]) for i in range(len(boxes)) if int(clss[i]) == 0]

                tracks = self.tracker.update_tracks(detections, frame=frame)

                for track in tracks:
                    # Detected Person
                    annotator = Annotator(frame, line_width=2)
                    self.create_label(annotator, track)
                    self.save_detected_person(track.track_id)

                    # Track
                    track_to_show = self.save_person_track_history(track)
                    self.show_person_track_history(frame, track_to_show)

                    self.save_track_history_database(track)

                    # Predict Track
                    estimated_velocity = self.calculate_velocity(track.track_id)
                    point = track_to_show[-1]

                    predicted_track = self.generate_predicted_track(point, estimated_velocity)
                    self.show_person_predicted_track(frame, predicted_track)

        self.check_person_visibility()


live_video_url = os.getenv("VIDEO_LIVE")
video_url = os.getenv("VIDEO")


def url_video():
    if os.getenv("VIDEO"):
        video = YouTube(os.getenv("VIDEO"))
        stream = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        return stream.url

    streams = streamlink.streams(os.getenv("VIDEO_LIVE"))
    return streams["best"].url


async def run_detection(websocket):
    device_cuda = 'cuda' if torch.cuda.is_available() else 'cpu'

    face_detector = FaceDetector('models/yolov8n-face.pt', device_cuda)
    person_detector = PersonDetector('models/yolov8n.pt', device_cuda)

    url = url_video()
    cap = cv2.VideoCapture(url)

    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Se terminaron los frames")

            person_detector.finish_person_visibility()
            cv2.destroyAllWindows()
            cap.release()
            break

        face_detector.detect_faces(frame)
        person_detector.detect_persons(frame)

        ret, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')

        data_to_send = {
            "image": jpg_as_text,
            "persons": person_detector.format_detected_persons()
        }

        json_data = json.dumps(data_to_send)

        await websocket.send(json_data)

    cap.release()


async def main():
    async with websockets.serve(run_detection, "localhost", 8772):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
