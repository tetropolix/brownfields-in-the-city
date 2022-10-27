from fastapi import FastAPI

app = FastAPI()


@app.get("/root/{id}")
async def root(id:int):
    return {"message": "Hello World"}
