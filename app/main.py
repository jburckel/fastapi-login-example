from fastapi import FastAPI
from app.endpoint import login, register, user

app = FastAPI()


app.include_router(
    login.router,
    prefix='/login'
)


app.include_router(
    register.router,
    prefix='/register'
)


app.include_router(
    user.router,
    prefix='/user'
)
