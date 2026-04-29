import requests

def detect_pothole(file, feature):
    API_URL = f"https://civic-lens-backend.onrender.com/detect/{feature}"

    files = {
        "file": (file.name, file.getvalue(), file.type)
    }

    response = requests.post(API_URL, files=files, timeout=120)

    return response