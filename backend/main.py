from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import FileResponse, RedirectResponse
from services.pothole import detect_pothole, detect_pothole_video
from services.flood import detect_flood, detect_flood_video

from starlette.middleware.sessions import SessionMiddleware
from auth.google_auth import oauth
from dotenv import load_dotenv

import shutil
import os
import uuid

load_dotenv()

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="supersecretkey123"
)

os.makedirs("outputs", exist_ok=True)


@app.get("/")
def home():
    return {"message": "Civic Lens API Running 🚀"}


# -------------------- POTHOLE IMAGE --------------------

@app.post("/detect/pothole")
async def pothole_api(file: UploadFile = File(...)):
    file_path = f"temp_{uuid.uuid4().hex}.jpg"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_path = detect_pothole(file_path)

    os.remove(file_path)

    return FileResponse(
        output_path,
        media_type="image/jpeg"
    )


# -------------------- FLOOD IMAGE --------------------

@app.post("/detect/flood")
async def flood_api(file: UploadFile = File(...)):
    file_path = f"temp_{uuid.uuid4().hex}.jpg"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_path = detect_flood(file_path)

    os.remove(file_path)

    return FileResponse(
        output_path,
        media_type="image/jpeg"
    )


# -------------------- POTHOLE VIDEO --------------------

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


# -------------------- FLOOD VIDEO --------------------

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


# -------------------- GOOGLE LOGIN --------------------

@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri
    )


@app.get("/auth/callback")
async def auth_callback(request: Request):

    token = await oauth.google.authorize_access_token(request)

    user = token.get("userinfo")

    if user:

        request.session["user"] = {
            "name": user.get("name"),
            "email": user.get("email"),
            "picture": user.get("picture")
        }

        return RedirectResponse(
            url="http://localhost:8501"
        )

    return {"error": "Login failed"}