import cv2
import numpy as np
import onnxruntime as ort
import base64
import websockets
import asyncio

import streamlink
import os
from dotenv import load_dotenv

from tracker import Tracker
from pytube import YouTube
load_dotenv()

# Inicializar el algoritmo de seguimiento
tracker = Tracker()

async def run_detection(websocket):

    # LIVE YOUTUBE
    # live_video_url = os.getenv("VIDEO")
    # streams = streamlink.streams(live_video_url)
    # url = streams["best"].url

    # VIDEO YOUTUBE
    video_url = os.getenv("VIDEO")
    video = YouTube(video_url)

    stream = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

    url = stream.url


    # Ruta al video que deseas procesar
    cap = cv2.VideoCapture(url)
    # video_url = 'https://www.youtube.com/watch?v=AoaLgrVn2vw'
    # cap = cv2.VideoCapture(video_url)

    ort_session = ort.InferenceSession('models/yolov8n.onnx')

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (640, 640))
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, axis=0)
        img_height, img_width = img.shape[:2]

        # ort_inputs = {ort_session.get_inputs()[0].name: img}
        # ort_outs = ort_session.run(None, ort_inputs)
        # detections = ort_outs[0]


        model_inputs = ort_session.get_inputs()
        input_shape = model_inputs[0].shape
        input_width = input_shape[2]
        input_height = input_shape[3]
        outputs = ort_session.run(None, {model_inputs[0].name: img})

        output = np.transpose(np.squeeze(outputs[0]))

        print(output)

        # Get the number of rows in the outputs array
        rows = output.shape[0]

        # Lists to store the bounding boxes, scores, and class IDs of the detections
        boxes = []
        scores = []
        class_ids = []

        # Calculate the scaling factors for the bounding box coordinates
        x_factor = img_width / input_width
        y_factor = img_height / input_height

        # Iterate over each row in the outputs array
        for i in range(rows):
            print(output)
            # Extract the class scores from the current row
            classes_scores = outputs[i][4:]

            # Find the maximum score among the class scores
            max_score = np.amax(classes_scores)

            # If the maximum score is above the confidence threshold
            if max_score >= 0.5:
                # Get the class ID with the highest score
                class_id = np.argmax(classes_scores)

                # Extract the bounding box coordinates from the current row
                x, y, w, h = outputs[i][0], outputs[i][1], outputs[i][2], outputs[i][3]

                # Calculate the scaled coordinates of the bounding box
                left = int((x - w / 2) * x_factor)
                top = int((y - h / 2) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)

                # Add the class ID, score, and box coordinates to the respective lists
                class_ids.append(class_id)
                scores.append(max_score)
                boxes.append([left, top, width, height])


        for detection in detections:
            print("Detection:" + str(detection))
            print("Detection type:" + str(type(detection)))
            print("Detection length:" + str(len(detection)))
            for obj in detection:
                print("Object:" + str(obj))
                print("Object type:" + str(type(obj)))
                print("Object length:" + str(len(obj)))
                if obj is not None:
                    x1, y1, x2, y2, conf, cls = obj
                    x1 = int(x1 * frame.shape[1])
                    y1 = int(y1 * frame.shape[0])
                    x2 = int(x2 * frame.shape[1])
                    y2 = int(y2 * frame.shape[0])

                detections = []

        # Aplicar el algoritmo de seguimiento
        tracker.update(frame, detections)

        # Dibujar los cuadros delimitadores y etiquetas de clase
        for track in tracker.tracks:
            bbox = track[:4]
            track_id = int(track[4])
            label = int(track[5])
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            cv2.putText(frame, f'Track ID: {track_id}', (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2)


        # for detection in detections:
        #     print(detection)
        #     x1, y1, x2, y2, conf, cls = detection
        #     if cls == 0:
        #         cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
        await websocket.send(jpg_as_text)

    cap.release()


async def main():
    async with websockets.serve(run_detection, "localhost", 8772):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
