from pydantic import BaseModel, Field
from datetime import datetime
# from enum import Enum
from typing import List

class VehicleSchema(BaseModel):
    timestamp: datetime
    vehicleType: str
    plateNumber: str
    plateCity: str

    class Config:
        orm_mode = True

class Vehicle(VehicleSchema):
    id: str

class Vehicleslimit(BaseModel):
    limit: int = Field(default=5)
    offset: int = Field(default=0)
    data: List[Vehicle]