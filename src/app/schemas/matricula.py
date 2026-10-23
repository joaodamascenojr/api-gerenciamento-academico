from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class MatriculaCreate(BaseModel):
    aluno_id: int = Field(gt=0)
    disciplina_id: int = Field(gt=0)


class MatriculaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    aluno_id: int
    disciplina_id: int
    data_matricula: date
