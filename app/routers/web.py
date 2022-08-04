import json
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Depends, HTTPException, Request, APIRouter, status
from starlette.responses import RedirectResponse, Response
import aiohttp
from app.token import verify_token


router_3 = APIRouter(
    include_in_schema=False
)

templates = Jinja2Templates(directory="app/templates")

url = 'http://localhost:8000'

def get_current_user(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        return None
    else:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No es posible validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )

        return verify_token(token, credentials_exception)

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

@router_3.get("/login_web")
async def login_web(request: Request):
    msj = ''
    return templates.TemplateResponse("login.html", {"request": request, 'msj': msj})

@router_3.get("/salir")
async def salir(request: Request, response: Response):
    msj = ''
    response = RedirectResponse(url='/', status_code=302)
    response.delete_cookie(key='access_token')
    return response

@router_3.post("/login_web")
async def login_web(request: Request, response: Response):
    form = await request.form()
    usuario = {
        'username': form.get('username'),
        'password': form.get('password')
    }
    url_post = f'{url}/login'
    async with aiohttp.ClientSession() as session:
        response = await session.request(method='POST', url=url_post, data=usuario)
        response_json = await response.json()
        
        if 'access_token' not in response_json:
            msj = 'Usuario o ontraseña incorrectos'
            return templates.TemplateResponse("login.html", {"request": request, 'msj': msj})
        
        response = RedirectResponse(url='/', status_code=302)
        response.set_cookie(key='access_token', value=response_json['access_token'])
        return response 

@router_3.get("/mostrar_usuarios")
async def mostrar_usuarios(request: Request, current_user= Depends(get_current_user)):
    msj = ''
    if current_user:
        return templates.TemplateResponse("mostrar_usuarios.html", {"request": request, 'msj': msj})
    else:
        response = RedirectResponse(url='/', status_code=302)
        #response = RedirectResponse(url='/').render(content='No tiene acceso a la pagina. Por favor inicie sesión')
        return response