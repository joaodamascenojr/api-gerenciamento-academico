from datetime import date

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Aluno(Base):
    __tablename__ = "alunos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(unique=True)
    data_nascimento: Mapped[date | None]

    matriculas: Mapped[list["Matricula"]] = relationship(
        back_populates="aluno", cascade="all, delete-orphan"
    )


class Disciplina(Base):
    __tablename__ = "disciplinas"

    id: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str] = mapped_column(unique=True)
    nome: Mapped[str]
    carga_horaria: Mapped[int]

    matriculas: Mapped[list["Matricula"]] = relationship(
        back_populates="disciplina", cascade="all, delete-orphan"
    )


class Matricula(Base):
    __tablename__ = "matriculas"
    __table_args__ = (UniqueConstraint("aluno_id", "disciplina_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    aluno_id: Mapped[int] = mapped_column(ForeignKey("alunos.id"))
    disciplina_id: Mapped[int] = mapped_column(ForeignKey("disciplinas.id"))
    data_matricula: Mapped[date] = mapped_column(default=date.today)

    aluno: Mapped[Aluno] = relationship(back_populates="matriculas")
    disciplina: Mapped[Disciplina] = relationship(back_populates="matriculas")
