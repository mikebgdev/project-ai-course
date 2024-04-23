import cv2
import uuid
import datetime

from ultralytics import YOLO


class Yolov8FaceService:
    def __init__(self, path_model):
        self.model = YOLO(path_model)
        self.blur_ratio = 50

    def create_data_to_csv(self, frame_id, box):
        return [
            str(uuid.uuid4()),
            frame_id,
            box.tolist(),
            datetime.datetime.now().timestamp()
        ]

    def detect_faces_and_blur(self, frame, frame_id):
        results = self.model.predict(frame, conf=0.4, verbose=False)

        # boxes = results[0].boxes

        boxes = results[0].boxes.xyxy.cpu()
        data_csv = None

        for box in boxes:
            face = frame[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
            blur_obj = cv2.blur(face, (self.blur_ratio, self.blur_ratio))

            frame[int(box[1]):int(box[3]), int(box[0]):int(box[2])] = blur_obj

            data_csv = self.create_data_to_csv(frame_id, box)

        return data_csv
