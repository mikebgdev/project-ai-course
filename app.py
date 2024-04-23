import cv2
import numpy as np

import uuid
import datetime

from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors

from collections import defaultdict
import mediapipe as mp

from src.blurred_face_service import blurred_person_face
from src.csv_manager import CSVFileManager
from tools.dit_tools import create_dir


def get_time_on_screen(track_id):
    if track_id in track_start_time:
        time_on_screen = datetime.datetime.now() - track_start_time[track_id]
        hours, remainder = divmod(time_on_screen.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02}:{:02}:{:02}".format(hours, minutes, seconds)
    else:
        return "00:00:00"


# Función para detectar y rastrear personas
def detect_and_track_person(frame, frame_id):
    results = model.track(frame, conf=0.8, persist=True, verbose=False)
    boxes = results[0].boxes.xyxy.cpu()

    if results[0].boxes.id is not None:
        clss = results[0].boxes.cls.cpu().tolist()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        confs = results[0].boxes.conf.cpu().tolist()

        annotator = Annotator(frame, line_width=2)

        for box, cls, track_id, conf in zip(boxes, clss, track_ids, confs):
            if int(cls) == 0:
                label = "Person{} - Time: {}".format(str(track_id), get_time_on_screen(track_id))
                annotator.box_label(box, color=colors(int(cls), True), label=label)

                # annotator.box_label(box, color=colors(int(cls), True), label=names[int(cls)])

                # Registra el tiempo de aparición de la persona
                if track_id not in track_start_time:
                    track_start_time[track_id] = datetime.datetime.now()

                # Registra la detección en el CSV dinámico
                csv_manager_dynamic.writer_row_csv(
                    csv_writer_dynamic,
                    [
                        str(uuid.uuid4()),  # UUID único para la detección
                        track_id,  # ID de seguimiento de la persona
                        frame_id,  # ID del fotograma
                        names[int(cls)],  # Clase de la persona
                        confs,  # Confianza de la detección
                        box.tolist(),  # Coordenadas de la caja delimitadora
                        datetime.datetime.now().timestamp()  # Fecha/hora de la detección (timestamp)
                    ]
                )

                track = track_history[track_id]
                track.append((int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)))
                if len(track) > 30:
                    track.pop(0)

                points = np.array(track, dtype=np.int32).reshape((-1, 1, 2))
                cv2.circle(frame, (track[-1]), 7, colors(int(cls), True), -1)
                cv2.polylines(frame, [points], isClosed=False, color=colors(int(cls), True), thickness=2)



# Prepare CSV
output_dir = create_dir("output")

# Crear instancias de CSVFileManager para archivos estáticos y dinámicos
csv_manager_static = CSVFileManager(output_dir + "detected_persons_static.csv")
csv_manager_dynamic = CSVFileManager(output_dir + "detected_persons_dynamic.csv")

header_static = ["UUID", "TrackID", "StartDate", "EndDate"]
header_dynamic = ["UUID", "TrackID", "FrameID", "Class", "Confidence", "Coordinates", "StartDate"]

csv_file_static = csv_manager_static.create_file_csv(header_static)
csv_file_dynamic = csv_manager_dynamic.create_file_csv(header_dynamic)

# Obtener escritores CSV
csv_writer_static = csv_manager_static.writer_file_csv(csv_file_static)
csv_writer_dynamic = csv_manager_dynamic.writer_file_csv(csv_file_dynamic)



track_history = defaultdict(lambda: [])
track_start_time = {}
model = YOLO("models/yolov8n.pt")
names = model.model.names

# face_cascade_model = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
assert cap.isOpened(), "Error reading video file"

w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

mp_face_detection = mp.solutions.face_detection

frame_id = 0
with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        success, frame = cap.read()
        if success:
            detect_and_track_person(frame, frame_id)
            frame_id += 1

            blurred_person_face(face_detection, frame)

            cv2.imshow("Project AI - Arch Btw", frame)

            # Registra las personas detectadas en el archivo CSV
            for track_id, start_time in track_start_time.items():
                if track_id not in track_history:  # La persona ha desaparecido de la pantalla
                    end_time = datetime.datetime.now()
                    csv_writer_static.writerow(
                        [str(uuid.uuid4()), track_id, start_time.timestamp(), end_time.timestamp()])
                    del track_start_time[track_id]

            if cv2.waitKey(1) & 0xFF == ord("q"):
                # Registra las personas detectadas en el archivo CSV
                for track_id, start_time in track_start_time.items():
                    end_time = datetime.datetime.now()
                    csv_writer_static.writerow(
                        [str(uuid.uuid4()), track_id, start_time.timestamp(), end_time.timestamp()])

                break
        else:
            break

csv_manager_static.close_csv_file(csv_file_static)
csv_manager_dynamic.close_csv_file(csv_file_dynamic)
cap.release()
cv2.destroyAllWindows()
