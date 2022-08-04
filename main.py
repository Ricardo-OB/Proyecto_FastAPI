from fastapi import FastAPI
import uvicorn
from app.routers import user, auth, web

app = FastAPI()
app.include_router(user.router_1)
app.include_router(auth.router_2)
app.include_router(web.router_3)

if __name__=='__main__':
    uvicorn.run('main:app', port=8000, reload=True)

