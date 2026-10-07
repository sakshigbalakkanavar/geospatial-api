from fastapi import FastAPI, UploadFile, File
from processor import read_file, calculate_measurements
import shutil
import uuid
from pathlib import Path

app = FastAPI()

files = {}


@app.get("/")
def home():
    return {"message": "Geospatial API is running"}


@app.post("/api/files/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith((".kml", ".zip")):
        return {"error": "Only KML and ZIP files are allowed"}

    file_id = str(uuid.uuid4())[:8]

    folder = Path("uploads")
    folder.mkdir(exist_ok=True)

    file_path = folder / file.filename

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        data = read_file(file_path)
        measurements = calculate_measurements(data)

        files[file_id] = {
            "id": file_id,
            "filename": file.filename,
            "features": len(data),
            "crs": str(data.crs),
            "measurements": measurements
        }

        return files[file_id]

    except Exception as e:
        return {"error": str(e)}


@app.get("/api/files/{file_id}")
def get_file(file_id: str):
    if file_id not in files:
        return {"error": "File not found"}

    return {
        "id": files[file_id]["id"],
        "filename": files[file_id]["filename"],
        "features": files[file_id]["features"],
        "crs": files[file_id]["crs"]
    }


@app.get("/api/files/{file_id}/measurements/")
def get_measurements(file_id: str):
    if file_id not in files:
        return {"error": "File not found"}

    return {
        "id": file_id,
        "measurements": files[file_id]["measurements"]
    }