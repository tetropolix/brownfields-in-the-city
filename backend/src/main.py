from fastapi import FastAPI
from routers import brownfields_router, auth_router
from fastapi_pagination import add_pagination
import globals  # check if all env variables were initialized

app = FastAPI()

app.include_router(auth_router.router)
app.include_router(brownfields_router.router)
add_pagination(app)
