from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from main import app
from app.db.models import Base
from app.hashing import Hash
from app.db.database import get_db

db_path = os.path.join(os.path.dirname(__file__), 'test.db')
SQLALCHEMY_DATABASE_URL = 'sqlite:///{}'.format(db_path)
engine_test = create_engine(url=SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(bind=engine_test, autocommit=False, autoflush=False)
Base.metadata.create_all(bind=engine_test)

cliente = TestClient(app)

def insertar_usuario_prueba():
    password_hash = Hash.hash_password('prueba123')
    engine_test.execute(
        f"""
        INSERT INTO usuario(username, password, nombre, apellido, direccion, telefono, correo)
        VALUES
        ('prueba', '{password_hash}', 'prueba_nombre', 'prueba_apellido', 'prueba_dir', 1211, 'prueba@f.com')
        """
    )

insertar_usuario_prueba()

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_crear_usuario():
    usuario = {
        "username": "ricardo23232",
        "password": "22",
        "nombre": "string",
        "apellido": "string",
        "direccion": "string",
        "telefono": 222,
        "correo": "a@mgil",
        "creacion_user": "2022-08-02T17:48:07.679221"
    }
    response_sin_token = cliente.post('/user/crear_usuario', json=usuario)
    assert response_sin_token.status_code == 401

    usuario_login = {
        'username': 'prueba',
        'password': 'prueba123'
    }
    response_token = cliente.post('/login/', data=usuario_login)
    assert response_token.status_code == 200
    assert response_token.json()['token_type'] == 'bearer'

    headers = {
        'Authorization': f"Bearer {response_token.json()['access_token']}"
    }
    response_con_token = cliente.post('/user/crear_usuario', json=usuario, headers=headers)
    assert response_con_token.status_code == 201
    assert response_con_token.json()['Respuesta'] == 'usuario creado satisfactoriamente'

def test_obtener_usuarios():
    response_sin_token = cliente.get('/user/')
    assert response_sin_token.status_code == 401

    usuario_login = {
        'username': 'prueba',
        'password': 'prueba123'
    }
    response_token = cliente.post('/login/', data=usuario_login)
    assert response_token.status_code == 200
    assert response_token.json()['token_type'] == 'bearer'

    headers = {
        'Authorization': f"Bearer {response_token.json()['access_token']}"
    }

    response_con_token = cliente.get('/user/', headers=headers)
    assert response_con_token.status_code == 200
    #print(response_con_token.json())

def test_obtener_usuario():
    response = cliente.get('/user/1')
    assert response.json()['username'] == 'prueba'

def test_eliminar_usuario():
    response = cliente.delete('/user/1')
    response_2 = cliente.get('/user/1')
    assert response.json()['Respuesta'] == 'Usuario eliminado satisfactoriamente'
    assert response_2.json()['detail'] == 'No existe el usuario con el ID 1'

def test_actualizar_usuario():
    usuario_actualizado = {
        "username": "user_actualizado"
    }
    response = cliente.patch('/user/2', json=usuario_actualizado)
    response_2 = cliente.get('/user/2')
    response_user_no_exist = cliente.patch('/user/999', json=usuario_actualizado)
    assert response.json()['Respuesta'] == 'Usuario actualizado correctamente'
    assert response_2.json()['username'] == 'user_actualizado'
    assert response_2.json()['nombre'] == 'string'
    assert response_user_no_exist.json()['detail'] == 'No existe el usuario con el ID 999'

def test_delete_database():
    db_path = os.path.join(os.path.dirname(__file__), 'test.db')
    os.remove(db_path)