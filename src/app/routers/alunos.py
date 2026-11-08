from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
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


@router.post(
    "/",
    response_model=AlunoRead,
    status_code=status.HTTP_201_CREATED,
)
def criar_aluno(dados: AlunoCreate, db: DbSession):
    if db.scalar(select(Aluno).where(Aluno.email == dados.email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "E-mail já cadastrado")

    aluno = Aluno(**dados.model_dump())
    db.add(aluno)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT, "E-mail já cadastrado"
        ) from None
    db.refresh(aluno)
    return aluno


@router.get("/", response_model=list[AlunoRead])
def listar_alunos(
    db: DbSession,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    return db.scalars(
        select(Aluno).order_by(Aluno.id).offset(skip).limit(limit)
    ).all()


@router.get("/{aluno_id}", response_model=AlunoRead)
def buscar_aluno(aluno_id: int, db: DbSession):
    return get_aluno_or_404(aluno_id, db)


@router.patch("/{aluno_id}", response_model=AlunoRead)
def atualizar_aluno(aluno_id: int, dados: AlunoUpdate, db: DbSession):
    aluno = get_aluno_or_404(aluno_id, db)
    campos = dados.model_dump(exclude_unset=True, exclude_none=True)

    if "email" in campos:
        email_existente = db.scalar(
            select(Aluno).where(
                Aluno.email == campos["email"],
                Aluno.id != aluno_id,
            )
        )
        if email_existente:
            raise HTTPException(
                status.HTTP_409_CONFLICT, "E-mail já cadastrado"
            )

    for campo, valor in campos.items():
        setattr(aluno, campo, valor)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT, "E-mail já cadastrado"
        ) from None
    db.refresh(aluno)
    return aluno


@router.delete("/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_aluno(aluno_id: int, db: DbSession):
    db.delete(get_aluno_or_404(aluno_id, db))
    db.commit()
