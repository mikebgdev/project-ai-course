import cv2


def blurred_frame(detection, frame, height, width):
    location_data = detection.location_data
    bbox = location_data.relative_bounding_box
    x1, y1, w, h = bbox.xmin, bbox.ymin, bbox.width, bbox.height
    x1, y1, w, h = int(x1 * width), int(y1 * height), int(w * width), int(h * height)

    face = frame[y1:y1 + h, x1:x1 + w]
    blurred_face = cv2.GaussianBlur(face, (99, 99), 20)
    frame[y1:y1 + h, x1:x1 + w] = blurred_face


def blurred_person_face(face_detection, frame):
    height, width, _ = frame.shape
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    out = face_detection.process(img_rgb)

    if out.detections is not None:
        for detection in out.detections:
            blurred_frame(detection, frame, height, width)
