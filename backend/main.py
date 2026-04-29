from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from services.pothole import detect_pothole, detect_pothole_video
from services.flood import detect_flood, detect_flood_video
import shutil
import os
import uuid

app = FastAPI()

os.makedirs("outputs", exist_ok=True)

@app.get("/")
def home():
    return {"message": "Civic Lens API Running 🚀"}


@app.post("/detect/pothole")
async def pothole_api(file: UploadFile = File(...)):
    file_path = f"temp_{uuid.uuid4().hex}.jpg"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_path = detect_pothole(file_path)
    os.remove(file_path)

    return FileResponse(output_path, media_type="image/jpeg")


@app.post("/detect/flood")
async def flood_api(file: UploadFile = File(...)):
    file_path = f"temp_{uuid.uuid4().hex}.jpg"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_path = detect_flood(file_path)
    os.remove(file_path)

    return FileResponse(output_path, media_type="image/jpeg")


@app.post("/detect/pothole-video")
async def pothole_video_api(file: UploadFile = File(...)):
    file_path = f"temp_{uuid.uuid4().hex}.mp4"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_path = detect_pothole_video(file_path)
    os.remove(file_path)

    return FileResponse(
        output_path,
        media_type="video/mp4",
        filename="result.mp4"
    )
    
@app.post("/detect/flood-video")
async def flood_video_api(file: UploadFile = File(...)):
    file_path = f"temp_{uuid.uuid4().hex}.mp4"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_path = detect_flood_video(file_path)
    os.remove(file_path)

    return FileResponse(
        output_path,
        media_type="video/mp4",
        filename="flood_result.mp4"
    )