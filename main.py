from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from ultralytics import YOLO
import io
from PIL import Image

app = FastAPI()
model = YOLO("models/best.pt")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Pagination"],
)


@app.get("/", tags=["Root"])
def root():
    return {"status": "OK", "message": "Hello World in AI PlantMed"}


@app.post("/predict", tags=["Predict"])
async def image_detection(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    results = model.predict(source=image, conf=0.5)
    im_array = results[0].plot()
    img = Image.fromarray(im_array[..., ::-1])
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()

    return Response(content=img_bytes, media_type="image/jpg")
