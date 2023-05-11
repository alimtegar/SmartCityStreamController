from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import DB_DIALECT, DB_DRIVER, DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, DB_SOCKET

#mysql+mysqlconnector://root:secret@db:3306/mysql?charset=utf8mb4
db_url = f'{DB_DIALECT}+{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4&unix_socket={DB_SOCKET}'
# print('db_url = ', db_url)
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
conn = engine.connect()