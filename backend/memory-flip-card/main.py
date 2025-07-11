from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

from database import engine, Base
import models
from routers import upload_router,list_router

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(upload_router.router)
app.include_router(list_router.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)