from fastapi import FastAPI

from app.routers import alunos, disciplinas, matriculas

app = FastAPI(title="API de Gerenciamento Acadêmico")

app.include_router(alunos.router)
app.include_router(disciplinas.router)
app.include_router(matriculas.router)


@app.get("/", tags=["Health"])
def read_root():
    return {"message": "API de Gerenciamento Acadêmico funcionando!"}
