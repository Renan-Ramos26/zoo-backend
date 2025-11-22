from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select, Relationship
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from typing import Optional, List

# --------------------- DATABASE ---------------------

DATABASE_URL = "sqlite:///./zoo.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# -------------------- MODELOS -----------------------

# Modelo para criação/atualização de ANIMAIS
class AnimalCreate(SQLModel):
    nome: str
    descricao: str
    data_nascimento: date
    especie: str
    habitat: str
    pais_origem: str

# Modelo para criação/atualização de CUIDADOS
class CuidadoCreate(SQLModel):
    nome: str
    descricao: str
    data: date
    animal_id: int  # 👈 quem recebe o cuidado

# Modelo Cuidado (salvo no banco)
class Cuidado(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    descricao: str
    data: date

    animal_id: int = Field(foreign_key="animal.id")
    animal: Optional["Animal"] = Relationship(back_populates="cuidados")

# Modelo Animal (salvo no banco)
class Animal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    descricao: str
    data_nascimento: date
    especie: str
    habitat: str
    pais_origem: str

    cuidados: List[Cuidado] = Relationship(back_populates="animal")

# --------------------- APP -------------------------

app = FastAPI()

# Habilitando CORS 🌍
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

# ------------------ ROTAS ANIMAL --------------------

@app.get("/animais")
def listar_animais(session: Session = Depends(get_session)):
    result = session.exec(select(Animal)).all()
    return result

@app.get("/animais/{animal_id}")
def buscar_animal(animal_id: int, session: Session = Depends(get_session)):
    animal = session.get(Animal, animal_id)
    if not animal:
        return {"erro": "Animal não encontrado"}
    return animal

@app.post("/animais")
def criar_animal(animal: AnimalCreate, session: Session = Depends(get_session)):
    novo = Animal(**animal.dict())
    session.add(novo)
    session.commit()
    session.refresh(novo)
    return {"mensagem": "Animal criado com sucesso", "animal": novo}

@app.put("/animais/{animal_id}")
def atualizar_animal(animal_id: int, dados: AnimalCreate, session: Session = Depends(get_session)):
    animal = session.get(Animal, animal_id)
    if not animal:
        return {"erro": "Animal não encontrado"}

    for campo, valor in dados.dict().items():
        setattr(animal, campo, valor)

    session.add(animal)
    session.commit()
    session.refresh(animal)
    return {"mensagem": "Animal atualizado", "animal": animal}

@app.delete("/animais/{animal_id}")
def deletar_animal(animal_id: int, session: Session = Depends(get_session)):
    animal = session.get(Animal, animal_id)
    if not animal:
        return {"erro": "Animal não encontrado"}
    session.delete(animal)
    session.commit()
    return {"mensagem": "Animal deletado com sucesso"}

# ------------------ ROTAS CUIDADOS ------------------

@app.get("/cuidados")
def listar_cuidados(session: Session = Depends(get_session)):
    return session.exec(select(Cuidado)).all()

@app.get("/cuidados/{cuidado_id}")
def buscar_cuidado(cuidado_id: int, session: Session = Depends(get_session)):
    cuidado = session.get(Cuidado, cuidado_id)
    if not cuidado:
        return {"erro": "Cuidado não encontrado"}
    return cuidado

@app.post("/cuidados")
def criar_cuidado(cuidado: CuidadoCreate, session: Session = Depends(get_session)):
    novo = Cuidado(**cuidado.dict())
    session.add(novo)
    session.commit()
    session.refresh(novo)
    return {"mensagem": "Cuidado criado com sucesso", "cuidado": novo}

@app.put("/cuidados/{cuidado_id}")
def atualizar_cuidado(cuidado_id: int, dados: CuidadoCreate, session: Session = Depends(get_session)):
    cuidado = session.get(Cuidado, cuidado_id)
    if not cuidado:
        return {"erro": "Cuidado não encontrado"}

    for campo, valor in dados.dict().items():
        setattr(cuidado, campo, valor)

    session.add(cuidado)
    session.commit()
    session.refresh(cuidado)
    return {"mensagem": "Cuidado atualizado", "cuidado": cuidado}

@app.delete("/cuidados/{cuidado_id}")
def deletar_cuidado(cuidado_id: int, session: Session = Depends(get_session)):
    cuidado = session.get(Cuidado, cuidado_id)
    if not cuidado:
        return {"erro": "Cuidado não encontrado"}
    session.delete(cuidado)
    session.commit()
    return {"mensagem": "Cuidado deletado com sucesso"}

@app.get("/")
def home():
    return {"mensagem": "API do Zoológico está funcionando! 🐾"}
