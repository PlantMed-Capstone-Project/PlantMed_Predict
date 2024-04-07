from pydantic import BaseModel
from datetime import datetime

class History(BaseModel):
    id: str
    full_name: str
    email: str
    plant_name: str
    created_date: datetime
    accuracy: float