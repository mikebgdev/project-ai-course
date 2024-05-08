import reflex as rx
import cv2
import streamlink

from ai_analsyis_flow_people.navigation import navbar
from ai_analsyis_flow_people.template import template
from ai_analsyis_flow_people.constants import blur_ratio, model_face, live_video_url


def init_video():
    streams = streamlink.streams(live_video_url)
    url = streams["best"].url

    cap = cv2.VideoCapture(url)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    assert cap.isOpened(), "Error reading video file"

    return cap


def detect_faces_and_blur(frame):
    results = model_face.track(frame, task='detect', conf=0.3, verbose=False)

    boxes = results[0].boxes.xyxy.cpu()
    confs = results[0].boxes.conf.cpu().tolist()

    for box, conf in zip(boxes, confs):
        face = frame[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
        blur_obj = cv2.blur(face, (blur_ratio, blur_ratio))

        frame[int(box[1]):int(box[3]), int(box[0]):int(box[2])] = blur_obj


def generate_frames():
    cap = init_video()

    if cap:
        while cap.isOpened():
            success, frame = cap.read()

            if not success:
                print("Se terminaron los frames")
                # finish_person_visibility()
                # cap_stop_video()
                break

            detect_faces_and_blur(frame)
            # detect_person_and_track(frame)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            return rx.obs.image(b'--frame\r\n'
                                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def content_video():
    return rx.video(
        url=live_video_url,
        width="640px",
        height="auto",
    )
    # return rx.box(
    #     generate_frames(),
    #     width=640,
    #     height=480
    # )


@template
def camera() -> rx.Component:
    return rx.box(
        navbar(heading="Live Camera"),
            rx.box(
                content_video(),
                margin_top="calc(50px + 2em)",
                padding="2em",
            ),
        padding_left="250px",
        # height="100vh"
    )
