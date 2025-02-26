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


