import cv2
import numpy as np

import uuid
import datetime

import mediapipe as mp

from src.blurred_face_service import BlurredFaceService
from src.csv_service import CSVManager
from src.yolov8_service import Yolov8Service
from tools.dit_tools import create_dir

# Prepare CSV
output_dir = create_dir("output")

csv_manager_static = CSVManager(output_dir + "detected_persons_static.csv")
csv_manager_frames = CSVManager(output_dir + "detected_persons_frames.csv")

header_static = ["UUID", "TrackID", "StartDate", "EndDate"]
header_frames = ["UUID", "TrackID", "FrameID", "Class", "Confidence", "Coordinates", "Date"]

csv_file_static = csv_manager_static.create_file_csv(header_static)
csv_file_frames = csv_manager_frames.create_file_csv(header_frames)

# Init Writers
csv_manager_static.writer_file_csv()
csv_manager_frames.writer_file_csv()

# Video WebCam
cap = cv2.VideoCapture(0)
assert cap.isOpened(), "Error reading video file"

w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

mp_face_detection = mp.solutions.face_detection


def save_track_csv_not_detected(csv_manager, tracks, tracks_history):
    for track_id, start_time in tracks.items():
        if track_id not in tracks_history:
            end_time = datetime.datetime.now()
            csv_manager.writer_row_csv(
                [str(uuid.uuid4()), track_id, start_time.timestamp(), end_time.timestamp()])
            del yolo_service.track_start_time[track_id]


def save_track_csv_finish_camera(csv_manager, tracks):
    for track_id, start_time in tracks.items():
        end_time = datetime.datetime.now()
        csv_manager.writer_row_csv(
            [str(uuid.uuid4()), track_id, start_time.timestamp(), end_time.timestamp()])


with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
    frame_id = 0
    yolo_service = Yolov8Service("models/yolov8n.pt")
    blurred_service = BlurredFaceService(face_detection)

    while cap.isOpened():
        success, frame = cap.read()
        if success:
            frame_id += 1

            data_frame_to_csv = yolo_service.detect_and_track_person(frame, frame_id)

            if data_frame_to_csv is not None:
                csv_manager_frames.writer_row_csv(data_frame_to_csv)

            blurred_service.blurred_person_face(frame)

            cv2.imshow("Project AI - Arch Btw", frame)

            save_track_csv_not_detected(csv_manager_static, yolo_service.track_start_time, yolo_service.track_history)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                save_track_csv_finish_camera(csv_manager_static, yolo_service.track_start_time)

                break
        else:
            break

csv_manager_static.close_csv_file(csv_file_static)
csv_manager_frames.close_csv_file(csv_file_frames)
cap.release()
cv2.destroyAllWindows()
