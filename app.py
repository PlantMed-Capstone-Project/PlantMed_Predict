"""
This file is to test Cyclic's hosting capabilities
"""

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from uuid import uuid4
import io
import uvicorn

app = FastAPI()
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


@app.post("/upload", tags=["Predict"])
async def upload_image(file: UploadFile = File(...)):
    file.filename = f"{uuid4()}.jpg"
    contents = await file.read()

    return StreamingResponse(io.BytesIO(contents), media_type="image/jpeg")


if __name__ == "__main__":
    uvicorn.run("app:app", port=5000, log_level="info")
