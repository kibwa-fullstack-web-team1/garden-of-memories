from fastapi import FastAPI
from database import engine, Base
from router import router as story_router
import models
import schemas
import crud
import uvicorn

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(story_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8011, reload=True)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    return {"status": 200, "message": "OK"} 