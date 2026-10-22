from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.deps import DbSession
from app.models import Disciplina
from app.schemas.disciplina import (
    DisciplinaCreate,
    DisciplinaRead,
    DisciplinaUpdate,
)

router = APIRouter(prefix="/disciplinas", tags=["Disciplinas"])


def get_disciplina_or_404(
    disciplina_id: int,
    db: Session,
) -> Disciplina:
    disciplina = db.get(Disciplina, disciplina_id)

    if not disciplina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disciplina não encontrada",
        )

    return disciplina


@router.post(
    "/",
    response_model=DisciplinaRead,
    status_code=status.HTTP_201_CREATED,
)
def create_disciplina(
    disciplina: DisciplinaCreate,
    db: DbSession,
):
    codigo_existente = db.scalar(
        select(Disciplina).where(Disciplina.codigo == disciplina.codigo)
    )

    if codigo_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe uma disciplina com esse código",
        )

    db_disciplina = Disciplina(**disciplina.model_dump())

    db.add(db_disciplina)
    db.commit()
    db.refresh(db_disciplina)

    return db_disciplina


@router.get("/", response_model=list[DisciplinaRead])
def read_disciplinas(
    db: DbSession,
    skip: int = 0,
    limit: int = 20,
):
    return db.scalars(
        select(Disciplina).order_by(Disciplina.id).offset(skip).limit(limit)
    ).all()


@router.get("/{disciplina_id}", response_model=DisciplinaRead)
def read_disciplina(
    disciplina_id: int,
    db: DbSession,
):
    return get_disciplina_or_404(disciplina_id, db)


@router.patch("/{disciplina_id}", response_model=DisciplinaRead)
def update_disciplina(
    disciplina_id: int,
    disciplina: DisciplinaUpdate,
    db: DbSession,
):
    db_disciplina = get_disciplina_or_404(disciplina_id, db)

    dados_atualizados = disciplina.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    if "codigo" in dados_atualizados:
        codigo_existente = db.scalar(
            select(Disciplina).where(
                Disciplina.codigo == dados_atualizados["codigo"],
                Disciplina.id != disciplina_id,
            )
        )

        if codigo_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe uma disciplina com esse código",
            )

    for campo, valor in dados_atualizados.items():
        setattr(db_disciplina, campo, valor)

    db.commit()
    db.refresh(db_disciplina)

    return db_disciplina


@router.delete(
    "/{disciplina_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_disciplina(
    disciplina_id: int,
    db: DbSession,
):
    db_disciplina = get_disciplina_or_404(disciplina_id, db)

    db.delete(db_disciplina)
    db.commit()
