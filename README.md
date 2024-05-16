# AI Project - Team Arch Btw

Web Reflex
```console
 reflex run
```

WebSocket
```console
python yolov8/websocket_server.py
```

## Final Project: Person Detection and Pixelation Application using YOLOv8n

This project was developed as part of the Specialization Course in Artificial Intelligence and Big Data

### Project Description

The project aims to utilize the YOLOv8n model for detecting and tracking people in a video environment. Additionally, it
implements face detection and pixelation to preserve the privacy of identified individuals.

### Key Features

- **Person Detection and Tracking:** Using the YOLOv8n model, the application can detect and track people in a real-time
  video stream.

- **Face Pixelation:** Using the YOLOv8n-face model, the application automatically detects the faces of identified
  individuals and applies a pixelation filter to protect their privacy.

### Technologies Used

- **YOLOv8n:** The YOLOv8n object detection model is utilized for identifying people in the video.

- **YOLOv8n-face:** The YOLOv8n-face object detection model is utilized for identifying people in the video.

- **Python:** The project is primarily developed in Python, leveraging the available libraries and tools in this
  language.

- **Flask:** The application is designed for use with Flask, providing a web interface to view live detection and pixelation functionalities.

### Usage Instructions

1. Install the necessary dependencies:

   ```console
   pip install -r requirements.txt
   ```

2. Run the application local:

   ```console
   python app.py
   ```

3. Run the application with flask:

   ```console
   flask run
   ```

### Tasks Pending

Task lists and roadmap: [Tasks](docs/Tasks.md)

### Authors

- Sergio Gimeno
- Michael Ballester

### References

- YOLOv8n: [Link to the official repository](https://github.com/ultralytics/ultralytics)
- YOLOv8n-faces [Link to the repository](https://github.com/akanametov/yolov8-face)
- Python Documentation: [Official website](https://docs.python.org/3/)
- Flask Documentation: [Official website](https://flask.palletsprojects.com/)
