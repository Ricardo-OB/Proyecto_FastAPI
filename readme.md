# Dos formas de ejecutar la App

1. Primera forma de ejecutar la app:
    app = FastAPI()
    
    Luego ejecutar uvicorn main:app

2. Segunda forma:
    if __name__=='__main__':
        uvicorn.run('main:app', port=8000, reload=True)

    Luego ejecutar main.py