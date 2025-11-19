from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import date
from fastapi.middleware.cors import CORSMiddleware

class Animal(BaseModel):
    id: Optional[int] = None
    nome: str
    descricao: str
    data_nascimento: date
    especie: str
    habitat: str
    pais_origem: str

app = FastAPI()

# HABILITANDO CORS 🚨
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

animais_db = []

@app.get("/animais")
def listar_animais():
    return animais_db

@app.post("/animais")
def criar_animal(animal: Animal):
    animal.id = len(animais_db) + 1
    animais_db.append(animal)
    return {"mensagem": "Animal criado com sucesso", "animal": animal}
