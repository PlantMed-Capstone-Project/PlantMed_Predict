from pydantic import BaseModel
from datetime import datetime


class MachineLeanring(BaseModel):
    id: str
    name: str


class DeepLearning(BaseModel):
    id: str
    name: str


class Model(BaseModel):
    id: str
    name: str
    accuracy: float
    is_active: bool
    machine_learning: MachineLeanring
    deep_learning: DeepLearning
    created_date: datetime
    updated_date: datetime


class ModelAll(BaseModel):
    id: str
    name: str
    accuracy: float
    is_active: bool
    machine_learning: MachineLeanring
    deep_learning: DeepLearning


class ModelRequest(BaseModel):
    name: str
    accuracy: float
    is_active: bool
    created_date: datetime
    updated_date: datetime
    machine_id: str
    deep_id: str


class ModelResponse(BaseModel):
    id: str
    file_url: str
    deep_name: str
