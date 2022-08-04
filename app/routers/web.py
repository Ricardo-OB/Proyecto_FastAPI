import json
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request, APIRouter
import requests
import aiohttp

router_3 = APIRouter()

templates = Jinja2Templates(directory="app/templates")

url = 'http://localhost:8000'

@router_3.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router_3.get("/register")
async def registration(request: Request):
    msj = ''
    return templates.TemplateResponse("create_user.html", {"request": request, 'msj': msj})

@router_3.post("/register")
async def registration(request: Request):
    form = await request.form()
    usuario = {
        'username': form.get('username'),
        'password': form.get('password'),
        'nombre': form.get('nombre'),
        'apellido': form.get('apellido'),
        'direccion': form.get('direccion'),
        'telefono': form.get('telefono'),
        'correo': form.get('correo')
    }
    url_post = f'{url}/user/crear_usuario'
    async with aiohttp.ClientSession() as session:
        response = await session.request(method='POST', url=url_post, json=usuario)
        response_json = await response.json()
        #print('Final: ', response_json)
        if 'Respuesta' in response_json:
            msj = 'Usuario creado satisfactoriamente'
            type_alert = 'success'
        else:
            msj = 'Usuario no fue creado'
            type_alert = 'danger'
        print(msj)
        return templates.TemplateResponse("create_user.html", {"request": request, 'msj': msj, 'type_alert': type_alert})