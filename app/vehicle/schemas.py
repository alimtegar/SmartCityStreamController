from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class VehicleSchema(BaseModel):
    timestamp: datetime
    vehicleType: str
    plateNumber: str
    plateCity: str
    stream_id: int

    class Config:
        orm_mode = True

class Vehicle(VehicleSchema):
    id: str

class Vehicleslimit(BaseModel):
    limit: int = Field(default=5)
    offset: int = Field(default=0)
    data: List[Vehicle]