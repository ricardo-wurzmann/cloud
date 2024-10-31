import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List
from utils import hash_password, verify_password
from jose import JWTError, jwt
from datetime import datetime, timedelta
import httpx
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv  # Importa a biblioteca dotenv

# Carregar as variáveis do arquivo .env
load_dotenv()

# Configurações do JWT
SECRET_KEY = os.getenv("SECRET_KEY", "YOUR_SECRET_KEY")  # Use uma chave secreta real
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

sec = HTTPBearer()

# Configuração do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL")  # Agora carrega do .env
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de usuário
class UserDB(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)

# Criação das tabelas
Base.metadata.create_all(bind=engine)

# Armazenamento em memória (substitua por um banco de dados em produção)
fake_users_db = {}

class User(BaseModel):
    nome: str
    email: str
    senha: str

class UserLogin(BaseModel):
    email: str
    senha: str

class Token(BaseModel):
    jwt: str

# Função para criar um token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para verificar o token JWT
def get_current_user(token: str = Depends(sec)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return email

@app.post("/registrar", response_model=Token)
def register_user(user: User):
    db = SessionLocal()  # Criar uma sessão do banco de dados
    if db.query(UserDB).filter(UserDB.email == user.email).first():
        raise HTTPException(status_code=409, detail="Email já registrado.")
    
    hashed_password = hash_password(user.senha)
    
    # Salvar no banco de dados
    new_user = UserDB(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    token = create_access_token(data={"sub": user.email})
    
    return {"jwt": token}

@app.post("/login", response_model=Token)
def login_user(user: UserLogin):
    db = SessionLocal()  # Criar uma sessão do banco de dados
    user_db = db.query(UserDB).filter(UserDB.email == user.email).first()

    if not user_db or not verify_password(user.senha, user_db.hashed_password):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos.")
    
    token = create_access_token(data={"sub": user.email})
    return {"jwt": token}

@app.get("/usuarios", response_model=List[str])
def get_users(authorization: HTTPAuthorizationCredentials = Depends(sec)):
    # O token é extraído diretamente do parâmetro authorization
    token = authorization.credentials  # O token JWT já está no formato correto

    # Validar o token
    credentials_exception = HTTPException(
        status_code=401,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Fazer uma requisição à API externa
    api_url = "https://global-patent1.p.rapidapi.com/s?ds=us&q=kettle"  # URL da API externa
    headers = {
        "x-rapidapi-host": "global-patent1.p.rapidapi.com",
        "x-rapidapi-key": "15cfe02b82msh84be3d25168c166p145b20jsn87329f715d09"  # Sua chave da API
    }

    response = httpx.get(api_url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Erro ao acessar a API externa")

    # Extrair os summaries das patentes
    data = response.json()  # Receber a resposta como JSON
    summaries = [patent['summary'] for patent in data.get('patents', [])]

    # Retornar apenas os summaries
    return summaries
