from fastapi import FastAPI
from database import engine, Base
from routers import question_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(question_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Daily Question Service"}
