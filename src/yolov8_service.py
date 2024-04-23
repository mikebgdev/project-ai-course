import cv2
import numpy as np
import uuid
import datetime
from collections import defaultdict

from ultralytics import YOLO
from ultralytics.solutions import object_counter
from ultralytics.utils.plotting import Annotator, colors


class Yolov8Service:
    def __init__(self, path_model):
        self.model = YOLO(path_model)
        self.names = self.model.model.names
        self.track_history = defaultdict(lambda: [])
        self.track_start_time = {}

    def get_time_on_screen(self, track_id):
        if track_id in self.track_start_time:
            time_on_screen = datetime.datetime.now() - self.track_start_time[track_id]
            hours, remainder = divmod(time_on_screen.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return "{:02}:{:02}:{:02}".format(hours, minutes, seconds)
        else:
            return "00:00:00"

    def create_label(self, annotator, track_id, box, cls):
        label = "Person{} - Time: {}".format(str(track_id), self.get_time_on_screen(track_id))
        annotator.box_label(box, color=colors(int(cls), True), label=label)

    def save_track_id(self, track_id):
        if track_id not in self.track_start_time:
            self.track_start_time[track_id] = datetime.datetime.now()

    def save_track_history(self, track_id, box):
        track = self.track_history[track_id]
        track.append((int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)))
        if len(track) > 30:
            track.pop(0)

        return track

    def show_track_history(self, frame, track, cls):
        points = np.array(track, dtype=np.int32).reshape((-1, 1, 2))
        cv2.circle(frame, (track[-1]), 7, colors(int(cls), True), -1)
        cv2.polylines(frame, [points], isClosed=False, color=colors(int(cls), True), thickness=2)

    def create_data_to_csv(self, track_id, frame_id, cls, confs, box):
        return [
            str(uuid.uuid4()),
            track_id,  #
            frame_id,
            self.names[int(cls)],  #
            confs,
            box.tolist(),
            datetime.datetime.now().timestamp()
        ]

    def detect_and_track_person(self, frame, frame_id):
        results = self.model.track(frame, conf=0.8, persist=True, verbose=False)
        boxes = results[0].boxes.xyxy.cpu()
        data_csv = None

        print(results[0].boxes)

        if results[0].boxes.id is not None:
            clss = results[0].boxes.cls.cpu().tolist()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            confs = results[0].boxes.conf.cpu().tolist()

            annotator = Annotator(frame, line_width=2)

            for box, cls, track_id, conf in zip(boxes, clss, track_ids, confs):
                if int(cls) == 0:
                    self.create_label(annotator, track_id, box, cls)

                    self.save_track_id(track_id)

                    track = self.save_track_history(track_id, box)

                    self.show_track_history(frame, track, cls)

                    data_csv = self.create_data_to_csv(track_id, frame_id, cls, confs, box)

        return data_csv
