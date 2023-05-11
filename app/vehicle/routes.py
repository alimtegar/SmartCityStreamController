from typing import Optional
from fastapi import APIRouter, Response, status
from fastapi.responses import HTMLResponse
from sqlalchemy import or_, and_
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
                        city: Optional[str] = None):
    
    print("Stream ID : ", stream_id)

    response_title = 'All Data'
    length = 0
    # Read Data by Stream ID 
    if stream_id is not None:
        # Filter Data by Time, time and type, time and city, and triple each Stream ID
        if time_start is not None and time_end is not None:
            if type is not None and city is None:
                query = vehicles.select().where(and_(vehicles.c.stream_id==stream_id, and_(vehicles.c.timestamp>=time_start, vehicles.c.timestamp<=time_end), vehicles.c.vehicleType == type))
                response_title = 'Count by TIME and TYPE in each stream ID'
            elif type is None and city is not None:
                query = vehicles.select().where(and_(vehicles.c.stream_id==stream_id, and_(vehicles.c.timestamp>=time_start, vehicles.c.timestamp<=time_end), vehicles.c.plateCity.contains(city)))
                response_title = 'Count by TIME and CITY in each stream ID'
            elif type is not None and city is not None:
                query = vehicles.select().where(and_(vehicles.c.stream_id==stream_id, and_(vehicles.c.timestamp>=time_start, vehicles.c.timestamp<=time_end), vehicles.c.plateCity.contains(city), vehicles.c.vehicleType == type))
                response_title = 'Count by TIME, CITY, and TYPE in each stream ID'
            else:
                query = vehicles.select().where(and_(vehicles.c.stream_id==stream_id, and_(vehicles.c.timestamp>=time_start, vehicles.c.timestamp<=time_end)))
                response_title = 'Count by TIME in each stream ID'

            data = conn.execute(query)

            result_dict = [u._asdict() for u in data.fetchall()]
            length = len(result_dict)
            response = {"message": f"success filter data ", "count": length, "data": result_dict}
        
        # Filter Data by Type and type & city each Stream ID
        elif type is not None:
            if city is not None:
                query = vehicles.select().where(and_(vehicles.c.stream_id==stream_id, vehicles.c.plateCity.contains(city), vehicles.c.vehicleType == type))
                response_title = 'Count by TYPE and CITY in each stream ID'
            else:
                query = vehicles.select().where(and_(vehicles.c.stream_id==stream_id, vehicles.c.vehicleType == type))
                response_title = 'Count by TYPE in each stream ID'
            data = conn.execute(query)

            result_dict = [u._asdict() for u in data.fetchall()]
            length = len(result_dict)
            response = {"message": f"success filter data ", "count": length, "data": result_dict}
        
        # Filter Data by City each Stream ID
        elif city is not None:
            query = vehicles.select().where(and_(vehicles.c.stream_id==stream_id, vehicles.c.plateCity.contains(city)))
            data = conn.execute(query)

            result_dict = [u._asdict() for u in data.fetchall()]
            length = len(result_dict)
            response_title = 'Count by CITY in each stream ID'
            response = {"message": f"success filter data ", "count": length, "data": result_dict}
        
        else:
            query = vehicles.select().where(vehicles.c.stream_id==stream_id)
            data = conn.execute(query)

            result_dict = [u._asdict() for u in data.fetchall()]
            length = len(result_dict)
            response_title = 'Count by stream ID'
            response = {"message": f"success get data ", "count": length, "data": result_dict }
        
        # return response if length !=0 else {"message": f"data not found"}

    # Filter Data by Time 
    if time_start is not None and time_end is not None:
        if type is not None and city is None:
            query = vehicles.select().where(and_(and_(vehicles.c.timestamp>=time_start, vehicles.c.timestamp<=time_end), vehicles.c.vehicleType == type))
            response_title = 'Count by TIME and TYPE'
        elif type is None and city is not None:
            query = vehicles.select().where(and_(and_(vehicles.c.timestamp>=time_start, vehicles.c.timestamp<=time_end), vehicles.c.plateCity.contains(city)))
            response_title = 'Count by TIME and CITY'
        elif type is not None and city is not None:
            query = vehicles.select().where(and_(and_(vehicles.c.timestamp>=time_start, vehicles.c.timestamp<=time_end), vehicles.c.plateCity.contains(city), vehicles.c.vehicleType == type))
            response_title = 'Count by TIME, CITY, and TYPE'
        else:
            query = vehicles.select().where(and_(vehicles.c.timestamp>=time_start, vehicles.c.timestamp<=time_end))
            response_title = 'Count by TIME'

        data = conn.execute(query)

        result_dict = [u._asdict() for u in data.fetchall()]
        length = len(result_dict)
        response = {"message": f"success filter data ", "count": length, "data": result_dict}
        
    # Filter Data by Type
    elif type is not None:
        if city is not None:
            query = vehicles.select().where(and_(vehicles.c.vehicleType == type, vehicles.c.plateCity.contains(city)))
            response_title = 'Count by TYPE and CITY'
        else:
            query = vehicles.select().where(vehicles.c.vehicleType == type)
            response_title = 'Count by TYPE'
        
        data = conn.execute(query)

        result_dict = [u._asdict() for u in data.fetchall()]
        length = len(result_dict)
        response = {"message": f"success filter data ", "count": length, "data": result_dict}
        
    # Filter Data by City
    elif city is not None:
        query = vehicles.select().where(vehicles.c.plateCity.contains(city))
        data = conn.execute(query)

        result_dict = [u._asdict() for u in data.fetchall()]
        length = len(result_dict)
        response_title = 'Count by CITY'
        response = {"message": f"success filter data ", "count": length, "data": result_dict}

    else:
        query = vehicles.select().offset(0).limit(10)
        data = conn.execute(query)

        response_title = 'Count All Vehicles'
        result_dict = [u._asdict() for u in data.fetchall()]
        length = len(result_dict)
        response = {"message": f"success read data", "data": result_dict}
    
    return response if length !=0 else {"message": f"data not found"}

    # html = f"""
    # <!DOCTYPE html>
    # <html>
    #     <head><title>Data Monitoring</title></head>
    #     <body>
    #         <h2>{response_title}</h2
    #         <h3>
    #             <strong>{length}</strong> vehicles counted.
    #         </h3>
    #     </body>
    # </html>
    # """
    # return HTMLResponse(content=html, status_code=200) 

@router.get("/{id}", description="Get the detail of a single vehicle.")
async def get_vehicle(id: str, response: Response):
    query = vehicles.select().where(vehicles.c.id == id)
    data = conn.execute(query).fetchone()
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