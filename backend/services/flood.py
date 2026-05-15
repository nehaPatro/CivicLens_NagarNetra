from ultralytics import YOLO
import os
import uuid
import cv2

# ABSOLUTE MODEL PATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "flood.pt")

# LOAD MODEL
model = YOLO(MODEL_PATH)

# DEBUG
print("Flood model loaded successfully")
print("Classes:", model.names)


def detect_flood(image_path):
    os.makedirs("outputs", exist_ok=True)

    results = model.predict(
        source=image_path,
        conf=0.05,
        imgsz=640
    )

    # DEBUG DETECTIONS
    print("Flood detections:", results[0].boxes)

    output_path = f"outputs/flood_{uuid.uuid4().hex}.jpg"

    # DRAW DETECTIONS
    annotated = results[0].plot()

    cv2.imwrite(output_path, annotated)

    return output_path


def detect_flood_video(video_path):
    os.makedirs("outputs", exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise Exception("Error opening video")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps == 0:
        fps = 20

    output_path = f"outputs/flood_video_{uuid.uuid4().hex}.mp4"

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height)
    )

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        results = model.predict(
            source=frame,
            conf=0.05,
            imgsz=640
        )

        # DEBUG
        print("Video detections:", results[0].boxes)

        annotated = results[0].plot()

        out.write(annotated)

    cap.release()
    out.release()

    return output_path