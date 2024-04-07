import io
import pyodbc
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from predict.predict import YoloPredict, EfficientNetV2Predict
from predict.loadModel import LoadModel

app = FastAPI()

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=PlantMed;UID=sa;PWD=123456;"
)

sql = conn.cursor()


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
async def image_detection(file: UploadFile = File(...), modelName: str = "YOLO"):
    try:
        if modelName == "YOLO":
            image = Image.open(io.BytesIO(await file.read()))
            response = YoloPredict(image, sql)
        elif modelName == "EfficientNet":
            input = EfficientNetV2Predict(file)
            response = LoadModel(input)
        else:
            response = "unknow"

        return JSONResponse(response)
    except:
        raise HTTPException(status_code=500, detail="An error occurred in predict")
