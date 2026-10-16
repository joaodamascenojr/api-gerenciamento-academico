from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr


class AlunoCreate(BaseModel):
    nome: str
    email: EmailStr
    data_nascimento: date | None = None


class AlunoUpdate(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    data_nascimento: date | None = None


class AlunoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: EmailStr
    data_nascimento: date | None
