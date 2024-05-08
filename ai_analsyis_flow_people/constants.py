import os

from ultralytics import YOLO
from dotenv import load_dotenv

load_dotenv()

model_face = YOLO('models/yolov8n-face.pt')
blur_ratio = 50
live_video_url = os.getenv("VIDEO")
