from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.deps import DbSession
from app.models import Aluno
from app.schemas.aluno import AlunoCreate, AlunoRead, AlunoUpdate

router = APIRouter(prefix="/alunos", tags=["Alunos"])


def get_aluno_or_404(aluno_id: int, db: Session) -> Aluno:
    aluno = db.get(Aluno, aluno_id)
    if not aluno:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Aluno não encontrado")
    return aluno


@router.post("/", response_model=AlunoRead, status_code=201)
def criar_aluno(dados: AlunoCreate, db: DbSession):
    if db.scalar(select(Aluno).where(Aluno.email == dados.email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "E-mail já cadastrado")
    aluno = Aluno(**dados.model_dump())
    db.add(aluno)
    db.commit()
    db.refresh(aluno)
    return aluno


@router.get("/", response_model=list[AlunoRead])
def listar_alunos(db: DbSession, skip: int = 0, limit: int = 20):
    return db.scalars(select(Aluno).offset(skip).limit(limit)).all()


@router.get("/{aluno_id}", response_model=AlunoRead)
def buscar_aluno(aluno_id: int, db: DbSession):
    return get_aluno_or_404(aluno_id, db)


@router.patch("/{aluno_id}", response_model=AlunoRead)
def atualizar_aluno(aluno_id: int, dados: AlunoUpdate, db: DbSession):
    aluno = get_aluno_or_404(aluno_id, db)
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(aluno, campo, valor)
    db.commit()
    db.refresh(aluno)
    return aluno


@router.delete("/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_aluno(aluno_id: int, db: DbSession):
    db.delete(get_aluno_or_404(aluno_id, db))
    db.commit()
