from typing import Optional
from fastapi import APIRouter, Response, status
from sqlalchemy import and_
from datetime import datetime

from app.database import conn
from .schemas import VehicleSchema
from .model import vehicles
from .dependencies import add_vehicle_to_db

router = APIRouter(prefix="/vehicles")

@router.get("/", description="Get the details of all vehicles")
async def get_vehicles(response: Response, stream_id: Optional[int] = None,
                        time_start: Optional[datetime] = None, time_end: Optional[datetime] = None,
                        type: Optional[str] = None,
                        city: Optional[str] = None,):
    # time_start = '2023-05-02 10:07:57'
    # time_end = '2023-05-02 10:23:36'
    print("Stream ID : ", stream_id)

    length = 0
    # Read Data by Stream ID 
    if stream_id is not None:
        # Filter Data by Time, time and type, time and city, and triple each Stream ID
        if time_start is not None and time_end is not None:
            if type is not None and city is None:
                query = vehicles.select().where(and_(vehicles.c.stream_id==stream_id, and_(vehicles.c.timestamp>=time_start, vehicles.c.timestamp<=time_end), vehicles.c.vehicleType == type))
            elif type is None and city is not None:
                query = vehicles.select().where(and_(vehicles.c.stream_id==stream_id, and_(vehicles.c.timestamp>=time_start, vehicles.c.timestamp<=time_end), vehicles.c.plateCity == city))
            elif type is not None and city is not None:
                query = vehicles.select().where(and_(vehicles.c.stream_id==stream_id, and_(vehicles.c.timestamp>=time_start, vehicles.c.timestamp<=time_end), vehicles.c.plateCity == city, vehicles.c.vehicleType == type))
            else:
                query = vehicles.select().where(and_(vehicles.c.stream_id==stream_id, and_(vehicles.c.timestamp>=time_start, vehicles.c.timestamp<=time_end)))
            
            data = conn.execute(query)

            result_dict = [dict(u) for u in data.fetchall()]
            length = len(result_dict)
            response = {"message": f"success filter data ", "count": length, "data": result_dict}
        
        # Filter Data by Type and type & city each Stream ID
        elif type is not None:
            if city is not None:
                query = vehicles.select().where(and_(vehicles.c.stream_id==stream_id, vehicles.c.plateCity == city, vehicles.c.vehicleType == type))
            else:
                query = vehicles.select().where(and_(vehicles.c.stream_id==stream_id, vehicles.c.vehicleType == type))
            data = conn.execute(query)

            result_dict = [dict(u) for u in data.fetchall()]
            length = len(result_dict)
            response = {"message": f"success filter data ", "count": length, "data": result_dict}
        
        # Filter Data by City each Stream ID
        elif city is not None:
            query = vehicles.select().where(and_(vehicles.c.stream_id==stream_id, vehicles.c.plateCity == city))
            data = conn.execute(query)

            result_dict = [dict(u) for u in data.fetchall()]
            length = len(result_dict)
            response = {"message": f"success filter data ", "count": length, "data": result_dict}
        
        else:
            query = vehicles.select().where(vehicles.c.stream_id==stream_id)
            data = conn.execute(query)

            result_dict = [dict(u) for u in data.fetchall()]
            length = len(result_dict)
            response = {"message": f"success get data ", "count": length, "data": result_dict }
        
        return response if length !=0 else {"message": f"data not found"}

    # Filter Data by Time 
    if time_start is not None and time_end is not None:
        if type is not None and city is None:
            query = vehicles.select().where(and_(and_(vehicles.c.timestamp>=time_start, vehicles.c.timestamp<=time_end), vehicles.c.vehicleType == type))
        elif type is None and city is not None:
            query = vehicles.select().where(and_(and_(vehicles.c.timestamp>=time_start, vehicles.c.timestamp<=time_end), vehicles.c.plateCity == city))
        elif type is not None and city is not None:
            query = vehicles.select().where(and_(and_(vehicles.c.timestamp>=time_start, vehicles.c.timestamp<=time_end), vehicles.c.plateCity == city, vehicles.c.vehicleType == type))
        else:
            query = vehicles.select().where(and_(vehicles.c.timestamp>=time_start, vehicles.c.timestamp<=time_end))
        
        data = conn.execute(query)

        result_dict = [dict(u) for u in data.fetchall()]
        length = len(result_dict)
        response = {"message": f"success filter data ", "count": length, "data": result_dict}
        
    # Filter Data by Type
    elif type is not None:
        if city is not None:
            query = vehicles.select().where(vehicles.c.plateCity == city)
        else:
            query = vehicles.select().where(vehicles.c.vehicleType == type)
        
        data = conn.execute(query)

        result_dict = [dict(u) for u in data.fetchall()]
        length = len(result_dict)
        response = {"message": f"success filter data ", "count": length, "data": result_dict}
        
    # Filter Data by City
    elif city is not None:
        query = vehicles.select().where(vehicles.c.plateCity == city)
        data = conn.execute(query)

        result_dict = [dict(u) for u in data.fetchall()]
        length = len(result_dict)
        response = {"message": f"success filter data ", "count": length, "data": result_dict}

    else:
        query = vehicles.select().offset(0).limit(10)
        data = conn.execute(query)
        result_dict = [dict(u) for u in data.fetchall()]
        length = len(result_dict)
        response = {"message": f"success read data", "data": result_dict}
    
    return response if length !=0 else {"message": f"data not found"}

@router.get("/{id}", description="Get the detail of a single vehicle.")
async def get_vehicle(id: int, response: Response):
    query = vehicles.select().where(vehicles.c.id == id)
    data = conn.execute(query).fetchone(dict())
    if data is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "data not found", "status": response.status_code}

    response = {"message": f"success fetching data by id {id}", "data": data }
    return response

@router.post('/', description="Add new vehicle.")
async def add_vehicle(vehicle : VehicleSchema):
    try:
        vehicle_dict = add_vehicle_to_db(vehicle)
        response = {
            'message': 'Vehicle added successfully.', 
            'data': vehicle_dict
        }
    except Exception as e:
        response = {'error': str(e)}
        
    return response