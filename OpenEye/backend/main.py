from fastapi import FastAPI, UploadFile
from workflow import run_workflow
from PIL import Image
import io

app = FastAPI()

@app.post("/analyze-eye")
async def analyze(file: UploadFile):

    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    result = run_workflow(image)

    return result