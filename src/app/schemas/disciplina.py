from pydantic import BaseModel, ConfigDict, Field


class DisciplinaCreate(BaseModel):
    codigo: str = Field(min_length=2, max_length=20)
    nome: str
    carga_horaria: int = Field(gt=0)


class DisciplinaUpdate(BaseModel):
    codigo: str | None = Field(default=None, min_length=2, max_length=20)
    nome: str | None = None
    carga_horaria: int | None = Field(default=None, gt=0)


class DisciplinaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    nome: str
    carga_horaria: int
