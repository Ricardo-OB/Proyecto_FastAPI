from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel

# User Model Schema
class User(BaseModel):
    username: str
    password: str
    nombre: str
    apellido: str
    direccion: Optional[str]
    telefono: int
    correo: str
    creacion_user: datetime = datetime.now()

class UpdateUser(BaseModel):
    username: str = None
    password: str = None
    nombre: str = None
    apellido: str = None
    direccion: str = None
    telefono: int = None
    correo: str = None

class ShowUser(BaseModel):
    username: str
    nombre: str
    apellido: str
    telefono: int
    correo: str
    class Config():
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None