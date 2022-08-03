from multiprocessing import synchronize
from fastapi import APIRouter, Depends, status
from app.oauth import get_current_user
from app.schemas import User, ShowUser, UpdateUser
from app.db.database import get_db
from sqlalchemy.orm import Session
from typing import List
from app.repository import user

router_1 = APIRouter(
    prefix='/user',
    tags=['Users']
)

@router_1.get('/', response_model=List[ShowUser], status_code=status.HTTP_200_OK)
def obtener_usuarios(db: Session=Depends(get_db), current_user: User = Depends(get_current_user)):
    data = user.obtener_usuarios(db)
    return data

@router_1.post('/crear_usuario', status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario:User, db: Session=Depends(get_db)):
    user.crear_usuario(usuario, db)
    return {'Respuesta': 'usuario creado satisfactoriamente'}

@router_1.get('/{user_id}', response_model=ShowUser, status_code=status.HTTP_200_OK) # se permite post o get
def obtener_usuario(user_id:int, db: Session=Depends(get_db)):
    usuario = user.obtener_usuario(user_id, db)
    return usuario

@router_1.delete('/{user_id}', status_code=status.HTTP_200_OK)
def eliminar_usuario(user_id: int, db: Session=Depends(get_db)):
    respuesta = user.eliminar_usuario(user_id, db)
    return respuesta

@router_1.patch('/{user_id}', status_code=status.HTTP_200_OK)
def actualizar_usuario(user_id: int, updateUser: UpdateUser, db: Session=Depends(get_db)):
    respuesta = user.actualizar_usuario(user_id, updateUser, db)
    return respuesta