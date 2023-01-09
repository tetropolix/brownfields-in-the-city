from fastapi import FastAPI
import globals  # check if all env variables were initialized
from routers import brownfields_router, auth_router
from fastapi_pagination import add_pagination
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:3000", "http://127.0.0.1:3000"] # for development purpose - used when direct communication with flask server is established

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router.router)
app.include_router(brownfields_router.router)
app.mount(
    "/static", StaticFiles(directory=globals.EnvVars.BROWNFIELDS_STATIC_DIR), name="static"
)
add_pagination(app)
