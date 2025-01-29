from src.models.vehiculo import Vehiculo
from sqlmodel import SQLModel, Session, create_engine

db_user: str = "quevedo"
db_password: str = "1234"
db_server: str = "db-mysql"
db_port: str = 3306
db_name: str = "vehiculodb"

DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
engine =create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Vehiculo(matricula="123456A",modelo="SEAT", km=100000))
        session.add(Vehiculo(matricula="123456B",modelo="HUNDAI", km=200000))
        session.add(Vehiculo(matricula="123456C",modelo="OPEL",  km=300000))
        session.add(Vehiculo(matricula="123456D",modelo="VW",  km=90000))
        session.add(Vehiculo(matricula="123456E",modelo="BMW",  km=80000))
        session.commit()       
                
