from ultralytics import YOLO
import os
import uuid
import cv2

model = YOLO("models/flood.pt")


def detect_flood(image_path):
    os.makedirs("outputs", exist_ok=True)

    results = model.predict(
        source=image_path,
        conf=0.37,   # your tuned value
        imgsz=640
    )

    output_path = f"outputs/flood_{uuid.uuid4().hex}.jpg"
    results[0].save(filename=output_path)

    return output_path


def detect_flood_video(video_path):
    os.makedirs("outputs", exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise Exception("Error opening video")

    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = cap.get(5) or 20

    output_path = f"outputs/flood_video_{uuid.uuid4().hex}.mp4"

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, conf=0.05)
        annotated = results[0].plot()

        out.write(annotated)

    cap.release()
    out.release()

    return output_path