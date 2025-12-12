from fastapi import FastAPI
from routers.users import user_router
from db.database import base,engine

base.metadata.create_all(bind=engine)

app=FastAPI()

@app.get("/")
def greet():
    return {"message":"Welcome to server"}

app.include_router(user_router)