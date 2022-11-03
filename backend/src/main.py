from fastapi import FastAPI
from routers import brownfields_router
import globals #check if all env variables were initialized

app = FastAPI()

app.include_router(brownfields_router.router)