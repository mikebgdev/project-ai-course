import cv2


class BlurredFaceService:
    def __init__(self, face_detection):
        self.face_detection = face_detection

    def blurred_frame(self, detection, frame, height, width):
        location_data = detection.location_data
        bbox = location_data.relative_bounding_box
        x1, y1, w, h = bbox.xmin, bbox.ymin, bbox.width, bbox.height
        x1 = max(int(x1 * width), 0)
        y1 = max(int(y1 * height), 0)
        w = max(int(w * width), 0)
        h = max(int(h * height), 0)

        face = frame[y1:y1 + h, x1:x1 + w]
        blurred_face = cv2.GaussianBlur(face, (99, 99), 40)
        frame[y1:y1 + h, x1:x1 + w] = blurred_face

    def blurred_person_face(self, frame):
        height, width, _ = frame.shape
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out = self.face_detection.process(img_rgb)

        if out.detections is not None:
            for detection in out.detections:
                self.blurred_frame(detection, frame, height, width)
