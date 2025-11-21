from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from typing import Optional

# --------------------- DATABASE ---------------------

DATABASE_URL = "sqlite:///./zoo.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# --------------------- MODELOS -----------------------

class Animal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    descricao: str
    data_nascimento: date
    especie: str
    habitat: str
    pais_origem: str

# 👉 Modelo usado para criar animais (sem ID)
class AnimalCreate(SQLModel):
    nome: str
    descricao: str
    data_nascimento: date
    especie: str
    habitat: str
    pais_origem: str

# --------------------- APP --------------------------

app = FastAPI()

# HABILITANDO CORS 🌍
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criar banco ao iniciar
@app.on_event("startup")
def on_startup():
    create_db()

# ------------------ ROTAS ---------------------------

@app.get("/animais")
def listar_animais(session: Session = Depends(get_session)):
    statement = select(Animal)
    result = session.exec(statement).all()
    return result

@app.post("/animais")
def criar_animal(animal: AnimalCreate, session: Session = Depends(get_session)):
    novo_animal = Animal(**animal.dict())  # cria usando dados do AnimalCreate
    session.add(novo_animal)
    session.commit()
    session.refresh(novo_animal)
    return {"mensagem": "Animal criado com sucesso", "animal": novo_animal}
