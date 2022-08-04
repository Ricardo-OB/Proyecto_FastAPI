from fastapi import FastAPI
import uvicorn
from app.routers import user, auth

app = FastAPI()
app.include_router(user.router_1)
app.include_router(auth.router_2)

# if __name__=='__main__':
#     uvicorn.run('main:app', port=8000, reload=True)

