# Counting berdasarkan waktu, jenis kendaraan, kota dari plat

from fastapi import APIRouter, Response, status
from sqlalchemy import or_, and_
from datetime import datetime
import mysql.connector

from app.database import conn, SessionLocal
from app.config import DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME, DB_PORT, DB_SOCKET
from .model import vehicles
from .schemas import VehicleSchema, Vehicleslimit

router = APIRouter()

db1 = mysql.connector.connect(
  host=DB_HOST,
  user=DB_USERNAME,
  passwd=DB_PASSWORD,
  database=DB_NAME,
  port=DB_PORT,
  unix_socket=DB_SOCKET,
)

session = SessionLocal()

@router.get("/vehicles/category/time", name="Filter by Time", description="Counting Data by Time")
async def counting_vehicles_time(time_start: datetime, time_end: datetime, response: Response):
    count_time = vehicles.select().where(and_(vehicles.c.timestamp>=time_start, vehicles.c.timestamp<=time_end))
    data = conn.execute(count_time)
    
    result_dict = [u._asdict() for u in data.fetchall()]
    length = len(result_dict)
    response = {"message": f"success filter data ", "count": length, "data": result_dict }
    print(len(result_dict))
    return response

@router.get("/vehicles/category/type", name="Filter by Type", description="Counting Data by Vehicle Type")
async def counting_vehicles_type(vtype: str,response: Response): 
    count_type = vehicles.select().where(vehicles.c.vehicleType == vtype)
    data = conn.execute(count_type)
    
    result_dict = [u._asdict() for u in data.fetchall()]
    length = len(result_dict)
    response = {"message": f"success filter data ", "count": length, "data": result_dict }
    print(len(result_dict))
    return response

@router.get("/vehicles/category/city", name="Filter by Plate City", description="Counting Data by Plate City")
async def counting_vehicles_city(vcity: str, response: Response): 
    count_city = vehicles.select().where(vehicles.c.plateCity == vcity)
    data = conn.execute(count_city)
    
    result_dict = [u._asdict() for u in data.fetchall()]
    length = len(result_dict)
    response = {"message": f"success filter data ", "count": length, "data": result_dict }
    print(len(result_dict))
    return response

@router.get("/vehicles/category/time-type", name="Filter by Time and Type", description="Counting Data by Time and Type")
async def counting_vehicles_time(time_start: datetime, time_end: datetime, vtype: str, response: Response):
    count_timetype = vehicles.select().where(and_(and_(vehicles.c.timestamp>=time_start, vehicles.c.timestamp<=time_end), vehicles.c.vehicleType == vtype))
    data = conn.execute(count_timetype)
    
    result_dict = [u._asdict() for u in data.fetchall()]
    length = len(result_dict)
    response = {"message": f"success filter data ", "count": length, "data": result_dict }
    print(len(result_dict))
    return response

@router.get("/vehicles/category/time-city", name="Filter by Time and Plate City", description="Counting Data by Time and PlateCity")
async def counting_vehicles_time(time_start: datetime, time_end: datetime, vcity: str, response: Response):
    count_timecity = vehicles.select().where(and_(and_(vehicles.c.timestamp>=time_start, vehicles.c.timestamp<=time_end)), vehicles.c.plateCity == vcity)
    data = conn.execute(count_timecity)
    
    result_dict = [u._asdict() for u in data.fetchall()]
    length = len(result_dict)
    response = {"message": f"success filter data ", "count": length, "data": result_dict }
    print(len(result_dict))
    return response

@router.get("/vehicles/category/city-type", name="Filter by Plate City and Type", description="Counting Data by Plate City and Type")
async def counting_vehicles_time(vtype: str, vcity: str, response: Response):
    count_citytype = vehicles.select().where(and_(vehicles.c.plateCity == vcity, vehicles.c.vehicleType == vtype))
    data = conn.execute(count_citytype)
    
    result_dict = [u._asdict() for u in data.fetchall()]
    length = len(result_dict)
    response = {"message": f"success filter data ", "count": length, "data": result_dict }
    print(len(result_dict))
    return response

@router.get("/vehicles/category/time-type-city", name="Filter by Time, Type, and Plate City", description="Counting Data By Time, Type, and Plate City")
async def counting_vehicles_time(time_start: datetime, time_end: datetime, vtype: str, vcity: str, response: Response):
    count_allcat = vehicles.select().where(and_(and_(vehicles.c.timestamp>=time_start, vehicles.c.timestamp<=time_end)), vehicles.c.plateCity == vcity, vehicles.c.vehicleType == vtype)
    data = conn.execute(count_allcat)
    
    result_dict = [u._asdict() for u in data.fetchall()]
    length = len(result_dict)
    response = {"message": f"success filter data ", "count": length, "data": result_dict }
    print(len(result_dict))
    return response

@router.get("/vehicles/all", response_model=Vehicleslimit, description="Read all data")
async def read_all_vehicles(limit: int = 10, offset: int = 0):
    query = vehicles.select().offset(offset).limit(limit)
    data = conn.execute(query).fetchall()
    response = {"limit": limit, "offset": offset, "data": data }
    return response

@router.get("/vehicles/{id}", name="Read Vehicle By ID", description="Show the detail of each data")
async def read_vehicle(id: int, response: Response):
    query = vehicles.select().where(vehicles.c.id == id)
    # print(vehicles.c)
    data = conn.execute(query).fetchone()._asdict()
    if data is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "not found", "status": response.status_code}

    response = {"message": f"success fetching data by id {id}", "data": data }
    return response

@router.post('/vehicles/add', description="Add new data")
async def insert_data(vhc : VehicleSchema, response: Response):
    cursor = db1.cursor(buffered=True)
    query = "INSERT INTO vehicles (id, vehicleType, plateNumber, plateCity, timestamp) VALUES (%s, %s, %s, %s, %s)"

    val = (vhc.id, vhc.vehicleType, vhc.plateNumber, vhc.plateCity, vhc.timestamp)
    cursor.execute(query, val)

    db1.commit()
    # with SessionLocal() as session:
    #     session.commit()
    # data = vehicles.select().order_by(vehicles.c.id.desc())
    data = "SELECT * FROM vehicles ORDER BY id DESC"
    cursor.execute(data)
    response = {"message": f"data successfully added", "data": cursor.fetchone()._asdict() } #.fetchone()._asdict()
    return response