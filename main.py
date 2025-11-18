from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import date

class Animal(BaseModel):
    id: Optional[int] = None
    nome: str
    descricao: str
    data_nascimento: date
    especie: str
    habitat: str
    pais_origem: str
app = FastAPI()

animais_db = []

@app.get("/")
def home():
    return {"mensagem": "API do Zoológico funcionando!"}

@app.post("/animais")
def criar_animal(animal: Animal):
    animal.id = len(animais_db) + 1
    animais_db.append(animal)
    return {"mensagem": "Animal criado com sucesso", "animal": animal}