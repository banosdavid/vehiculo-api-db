from sqlmodel import SQLModel, Field

class Vehiculo(SQLModel, table=True):
    matricula: str | None = Field(default=None, primary_key=True)
    modelo: str = Field(index=True, max_length=50)
    km: int =Field(nullable=True)

