from ultralytics import YOLO
import os
import uuid
import cv2

model = YOLO("models/pothole.pt")

def detect_pothole(image_path):
    os.makedirs("outputs", exist_ok=True)

    results = model.predict(
        source=image_path,
        conf=0.37,
        iou=0.4,
        imgsz=640
    )

    output_path = f"outputs/pothole_{uuid.uuid4().hex}.jpg"
    results[0].save(filename=output_path)

    return output_path


def detect_pothole_video(video_path):
    os.makedirs("outputs", exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = cap.get(5) or 20

    output_path = f"outputs/video_{uuid.uuid4().hex}.mp4"

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, conf=0.37)
        annotated = results[0].plot()

        out.write(annotated)

    cap.release()
    out.release()

    return output_path