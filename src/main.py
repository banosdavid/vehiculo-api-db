from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select, func
from contextlib import asynccontextmanager
from typing import Annotated

from src.models.vehiculo import Vehiculo
from src.data.db import get_session, init_db

@asynccontextmanager
async def lifespan(application: FastAPI):
    init_db()
    yield

SessionDep= Annotated [Session, Depends(get_session)]


app = FastAPI(lifespan=lifespan)


#vehiculo con menos kilometros

@app.get("/vehiculos/menoskm", response_model=Vehiculo)
async def vehiculo_menos_kilometros(session: SessionDep):
    vehiculos = session.exec(select(Vehiculo)).all()
    
    if not vehiculos:
        raise HTTPException(status_code=400, detail="No vehicles found")
    
    vehiculo_menos_km = None
    for vehiculo in vehiculos:
        if vehiculo_menos_km is None or vehiculo.km < vehiculo_menos_km.km:
            vehiculo_menos_km = vehiculo
    
    return vehiculo_menos_km





@app.get("/vehiculos/media")
async def calcular_media_kilometros(session: SessionDep):
    vehiculos = session.exec(select(Vehiculo)).all()
    
    
    if not vehiculos:
        raise HTTPException(status_code=400, detail="No vehicles found")
    total_km=0
    for vehiculo in vehiculos:
        total_km = vehiculo.km 
        media_km = total_km / len(vehiculos)
        return {"mediaKilometros": media_km}




@app.get("/vehiculos/media-sql")
def calcular_media_kilometros_sql(session: SessionDep):
    media = session.exec(select(func.avg(Vehiculo.km))).first()
    return {"mediaKilometros": media}
            


@app.delete("/vehiculos/{vehiculo_matricula}")
def delete_vehiculo(vehiculo_matricula: str, session: SessionDep):
    vehiculo_encontrado = session.get(Vehiculo, vehiculo_matricula)
    if not vehiculo_encontrado:
        raise HTTPException(status_code=404, detail="Vehiculo not found")
    session.delete(vehiculo_encontrado)
    session.commit()
    return {"Vehiculo deleted successfully"}





@app.get("/vehiculos", response_model=list[Vehiculo])
async def lista_vehiculos(session:SessionDep):
    vehiculos = session.exec(select(Vehiculo)).all()
    return vehiculos


@app.post("/vehiculos", response_model=Vehiculo)
async def nuevo_vehiculo(vehiculo:Vehiculo, session: SessionDep):
    session.add(vehiculo)
    session.commit()
    session.refresh(vehiculo)
    return vehiculo


@app.get("/vehiculos/{vehiculo_matricula}", response_model=Vehiculo)
def        read_vehiculo(vehiculo_matricula: str, session: SessionDep):
    vehiculo = session.get(Vehiculo, vehiculo_matricula)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehiculo not found")
    return vehiculo
    




@app.patch("/vehiculos/{vehiculo_matricula}", response_model=Vehiculo)
def update_vehiculo(vehiculo_matricula: str, vehiculo: Vehiculo, session: SessionDep):
    vehiculo_encontrado = session.get(Vehiculo, vehiculo_matricula)
    if not vehiculo_encontrado:
        raise HTTPException(status_code=404, detail="Vehiculo not found")
    vehiculo_data=vehiculo.model_dump(exclude_unset=True)
    vehiculo_encontrado.sqlmodel_update(vehiculo_data)
    session.add(vehiculo_encontrado)
    session.commit()
    session.refresh(vehiculo_encontrado)
    return vehiculo_encontrado



@app.put("/vehiculos", response_model=Vehiculo)
def update_vehiculo(vehiculo: Vehiculo, session: SessionDep):
    vehiculo_encontrado = session.get(Vehiculo, vehiculo.matricula)
    if not vehiculo_encontrado:
        raise HTTPException(status_code=404, detail="Vehiculo not found")
    vehiculo_data=vehiculo.model_dump()
    vehiculo_encontrado.sqlmodel_update(vehiculo_data)
    session.add(vehiculo_encontrado)
    session.commit()
    session.refresh(vehiculo_encontrado)
    return vehiculo_encontrado


