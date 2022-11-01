from fastapi import FastAPI
from routers import brownfields_router


app = FastAPI()

app.include_router(brownfields_router.router)