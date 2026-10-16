from fastapi import FastAPI

from app.routers import alunos

app = FastAPI(title="API de Gerenciamento Acadêmico")
app.include_router(alunos.router)


@app.get("/", tags=["Health"])
def read_root():
    return {"message": "API de Gerenciamento Acadêmico funcionando!"}
