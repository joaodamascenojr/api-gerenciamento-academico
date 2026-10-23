from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.deps import DbSession
from app.models import Aluno, Disciplina, Matricula
from app.schemas.matricula import MatriculaCreate, MatriculaRead

router = APIRouter(prefix="/matriculas", tags=["Matrículas"])


def get_matricula_or_404(matricula_id: int, db: Session) -> Matricula:
    matricula = db.get(Matricula, matricula_id)
    if not matricula:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Matrícula não encontrada"
        )
    return matricula


@router.post(
    "/",
    response_model=MatriculaRead,
    status_code=status.HTTP_201_CREATED,
)
def criar_matricula(dados: MatriculaCreate, db: DbSession):
    if not db.get(Aluno, dados.aluno_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Aluno não encontrado")

    if not db.get(Disciplina, dados.disciplina_id):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Disciplina não encontrada"
        )

    ja_matriculado = db.scalar(
        select(Matricula).where(
            Matricula.aluno_id == dados.aluno_id,
            Matricula.disciplina_id == dados.disciplina_id,
        )
    )
    if ja_matriculado:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Aluno já matriculado nesta disciplina",
        )

    matricula = Matricula(**dados.model_dump())
    db.add(matricula)
    db.commit()
    db.refresh(matricula)
    return matricula


@router.get("/", response_model=list[MatriculaRead])
def listar_matriculas(db: DbSession, skip: int = 0, limit: int = 20):
    return db.scalars(
        select(Matricula).order_by(Matricula.id).offset(skip).limit(limit)
    ).all()


@router.get("/{matricula_id}", response_model=MatriculaRead)
def buscar_matricula(matricula_id: int, db: DbSession):
    return get_matricula_or_404(matricula_id, db)


@router.delete("/{matricula_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_matricula(matricula_id: int, db: DbSession):
    db.delete(get_matricula_or_404(matricula_id, db))
    db.commit()
