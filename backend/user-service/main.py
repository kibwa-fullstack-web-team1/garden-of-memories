from fastapi import FastAPI
import uvicorn

from database import engine, Base
import models # models 패키지를 임포트하여 모든 모델이 Base에 등록되도록 합니다.
from routers import activity_router

# 모든 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(activity_router.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

@app.get("/health")
def healthCheck():
    """
    서버가 정상적으로 작동하는지 확인하는 API입니다.
    """
    print("health check")
    return {"status": 200, "message": "OK"}

@app.get("/")
def root():
    return {"message": "Hello World"}
