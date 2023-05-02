# Counting berdasarkan waktu, jenis kendaraan, kota dari plat

import uuid
from typing import Optional
from fastapi import APIRouter, Response, status
from sqlalchemy import and_
from datetime import datetime
# import mysql.connector

from app.database import conn, SessionLocal
# from app.config import DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME, DB_PORT, DB_SOCKET
from .model import vehicles
from .schemas import VehicleSchema, Vehicleslimit

router = APIRouter()

# db1 = mysql.connector.connect(
#   host=DB_HOST,
#   user=DB_USERNAME,
#   passwd=DB_PASSWORD,
#   database=DB_NAME,
#   port=DB_PORT,
#   unix_socket=DB_SOCKET,
# )

session = SessionLocal()

@router.get("/vehicles", description="Read vehicles data")
async def read_vehicles(response: Response, stream_id: Optional[int] = None,
                        time_start: Optional[datetime] = None, time_end: Optional[datetime] = None,
                        type: Optional[str] = None,
                        city: Optional[str] = None,):
    # time_start = '2023-05-02 10:07:57'
    # time_end = '2023-05-02 10:23:36'
    print("Stream ID : ", stream_id)

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

            result_dict = [u._asdict() for u in data.fetchall()]
            length = len(result_dict)
            response = {"message": f"success filter data ", "count": length, "data": result_dict}
        
        # Filter Data by Type and type & city each Stream ID
        elif type is not None:
            if city is not None:
                query = vehicles.select().where(and_(vehicles.c.stream_id==stream_id, vehicles.c.plateCity == city, vehicles.c.vehicleType == type))
            else:
                query = vehicles.select().where(and_(vehicles.c.stream_id==stream_id, vehicles.c.vehicleType == type))
            data = conn.execute(query)

            result_dict = [u._asdict() for u in data.fetchall()]
            length = len(result_dict)
            response = {"message": f"success filter data ", "count": length, "data": result_dict}
        
        # Filter Data by City each Stream ID
        elif city is not None:
            query = vehicles.select().where(and_(vehicles.c.stream_id==stream_id, vehicles.c.plateCity == city))
            data = conn.execute(query)

            result_dict = [u._asdict() for u in data.fetchall()]
            length = len(result_dict)
            response = {"message": f"success filter data ", "count": length, "data": result_dict}
        
        else:
            query = vehicles.select().where(vehicles.c.stream_id==stream_id)
            data = conn.execute(query)

            result_dict = [u._asdict() for u in data.fetchall()]
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

        result_dict = [u._asdict() for u in data.fetchall()]
        length = len(result_dict)
        response = {"message": f"success filter data ", "count": length, "data": result_dict}
        
    # Filter Data by Type
    elif type is not None:
        if city is not None:
            query = vehicles.select().where(vehicles.c.plateCity == city)
        else:
            query = vehicles.select().where(vehicles.c.vehicleType == type)
        
        data = conn.execute(query)

        result_dict = [u._asdict() for u in data.fetchall()]
        length = len(result_dict)
        response = {"message": f"success filter data ", "count": length, "data": result_dict}
        
    # Filter Data by City
    elif city is not None:
        query = vehicles.select().where(vehicles.c.plateCity == city)
        data = conn.execute(query)

        result_dict = [u._asdict() for u in data.fetchall()]
        length = len(result_dict)
        response = {"message": f"success filter data ", "count": length, "data": result_dict}

    else:
        query = vehicles.select().offset(0).limit(10)
        data = conn.execute(query)

        result_dict = [u._asdict() for u in data.fetchall()]
        response = {"message": f"success read data", "data": result_dict}
    
    return response if length !=0 else {"message": f"data not found"}

@router.get("/vehicles/{id}", name="Read Vehicle By ID", description="Show the detail of each data")
async def read_vehicle(id: int, response: Response):
    query = vehicles.select().where(vehicles.c.id == id)
    # print(vehicles.c)
    data = conn.execute(query).fetchone()._asdict()
    if data is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "data not found", "status": response.status_code}

    response = {"message": f"success fetching data by id {id}", "data": data }
    return response

@router.post('/vehicles', description="Add new vehicle")
async def insert_vehicle(vehicle : VehicleSchema):
    try:
        # Generate a UUID for the new vehicle record
        vehicle_id = str(uuid.uuid4())
        
        # Add the UUID to the vehicle data
        vehicle_dict = dict(vehicle)
        vehicle_dict['id'] = vehicle_id
        
        # Insert the new vehicle record into the database
        stmt = vehicles.insert().values(**vehicle_dict)
        session.execute(stmt)

        response = {"message": f"data successfully added", "data": vehicle_dict}
    except Exception as e:
        response = {"message": f"an error occurred: {str(e)}"}
    finally:
        session.close()

    return response