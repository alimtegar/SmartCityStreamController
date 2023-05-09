from datetime import datetime
from sqlalchemy import Table, Column, MetaData, String
from sqlalchemy.sql.sqltypes import DateTime

metadata = MetaData()

vehicles = Table(
    'vehicles', 
    metadata,
    Column('id', String(36), primary_key=True, index=True),
    Column('vehicleType', String(255)),
    Column('plateNumber', String(255)),
    Column('plateCity', String(255)),
    Column('streamId', String(36)),
    Column('timestamp', DateTime(), default=datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
)