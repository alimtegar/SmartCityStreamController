import uuid

from .schemas import VehicleSchema
from .model import vehicles

from app.database import conn

def add_vehicle_to_db(vehicle: VehicleSchema):
  try:
    # Generate a UUID for the new vehicle record
    vehicle_id = str(uuid.uuid4())
    
    # Add the UUID to the vehicle data
    vehicle_dict = dict(vehicle)
    vehicle_dict['id'] = vehicle_id
    
    # Insert the new vehicle record into the database
    query = vehicles.insert().values(**vehicle_dict)
    conn.execute(query)
    conn.commit()
    
    return vehicle_dict
  except Exception as e:
    raise e