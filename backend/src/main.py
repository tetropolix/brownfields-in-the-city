from fastapi import FastAPI
import globals  # check if all env variables were initialized
from globals import EnvVars
from routers import brownfields_router, auth_router
from fastapi_pagination import add_pagination
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(auth_router.router)
app.include_router(brownfields_router.router)
app.mount(
    "/static", StaticFiles(directory=EnvVars.BROWNFIELDS_STATIC_DIR), name="static"
)
add_pagination(app)
