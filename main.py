from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import io
from PIL import Image
import pyodbc
from collections import Counter

app = FastAPI()
model = YOLO("models/best.pt")

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=PlantMed;UID=sa;PWD=123456;"
)

sql = conn.cursor()


def get_by_name(name: str) -> dict:
    sql.execute("SELECT * FROM Plant WHERE name = ?", (name,))
    row = sql.fetchone()
    response = {
        "id": row.id.lower(),
        "name": row.name,
        "internationalName": row.international_name,
        "surName": row.sur_name,
        "placeOfBirth": row.place_of_birth,
        "shopBase": row.shop_base,
        "origin": row.origin,
        "usage": row.usage,
    }
    return response


def format(results: list) -> float:
    if not results:
        return 0.0

    map = {}
    for rs in results:
        if rs in map:
            map[rs] += 1
        else:
            map[rs] = 1

    if not map:
        return 0.0

    max_value = max(map.values())

    percentage = (max_value / len(results)) * 100
    return round(percentage, 2) if percentage else 0.0


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


@app.post("/predict/yolo", tags=["Predict"])
async def image_detection(file: UploadFile = File(...)):
    try:
        image = Image.open(io.BytesIO(await file.read()))
        results = model.predict(source=image, conf=0.5)

        class_result = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.data[0][-1])
                class_result.append(model.names[class_id])

        counter = Counter(class_result)
        most_common = counter.most_common(1)
        name = most_common[0][0]

        plant = get_by_name(name)
        acc_result = f"{format(class_result)}%"

        response = {"accuracy": acc_result, "plant": plant}

        return JSONResponse(response)
    except:
        raise HTTPException(status_code=500, detail="An error occurred in predict")


@app.post("/predict/tf", tags=["Predict"])
async def predict(file: UploadFile = File(...)):
    response = {}
    return response


async def save(data):
    try:
        pass
    except:
        raise HTTPException(status_code=500, detail="")
    pass
