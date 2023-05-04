from sqlalchemy import Table, Column, Integer, MetaData, String
from sqlalchemy.sql.sqltypes import DateTime

metadata = MetaData()

vehicles = Table(
    'vehicles', metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('vehicleType', String(255)), #Enum('Car', 'Bus', 'Motorcycle', 'Truck')),
    Column('plateNumber', String(255)),
    Column('plateCity', String(255)),
    Column('stream_id', Integer),
    Column('timestamp', DateTime()),
)