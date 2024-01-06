from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from uuid import uuid4
import io

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


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file.filename = f"{uuid4()}.jpg"
    contents = await file.read()

    data = StreamingResponse(io.BytesIO(contents), media_type="image/jpeg")
    if data is not None:
        return data
    else:
        raise HTTPException(status_code=400, detail="The request is not an image")

    # return StreamingResponse(io.BytesIO(contents), media_type="image/jpeg")

    # with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
    #     f.write(contents)

    # path = f"{IMAGEDIR}{file.filename}"

    # return FileResponse(path, media_type="image/jpeg")
