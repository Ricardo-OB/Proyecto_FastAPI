# Dos formas de ejecutar la App

1. Primera forma de ejecutar la app:
    app = FastAPI()
    
    Luego ejecutar uvicorn main:app

2. Segunda forma:
    if __name__=='__main__':
        uvicorn.run('main:app', port=8000, reload=True)

    Luego ejecutar main.py

# Realizar Migraciones

alembic init migrations

# Configurar Alembic

- Abrir el archivo alembic.ini y modificar la linea sqlalchemy.url (dejarla vacia)

# Abrir el env.py de la carpeta migrations

Copiar las siguientes lineas antes de la funcion run_migrations_offline

    from core.config import settings

    config = context.config
    config.set_main_option('sqlalchemy.url', settings.database_url)

    if config.config_file_name is not None:
        fileConfig(config.config_file_name)

    from app.db.models import Base
    target_metadata = Base.metadata 

# Por ultimo...

Correr/ejecutar las siguiente dos lineas

    alembic revision --autogenerate -m "Create models"
    alembic upgrade heads
