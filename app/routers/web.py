from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request, APIRouter

router_3 = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router_3.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router_3.get("/register")
async def registration(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})

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
    print(usuario)
    return templates.TemplateResponse("create_user.html", {"request": request})