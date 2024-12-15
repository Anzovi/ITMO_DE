from datetime import datetime

from pydantic import BaseModel


class SensorData(BaseModel):
    timestamp: datetime
    device: str
    amperage: float
