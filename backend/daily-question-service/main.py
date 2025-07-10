from fastapi import FastAPI
import uvicorn

from database import engine, Base
import models
from routers import question_router

# 모든 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="오늘의 질문 서비스",
    description="사용자에게 매일 개인화된 질문을 제공하고, 답변을 관리하는 API입니다.",
    version="0.1.0"
)

app.include_router(question_router.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)

@app.get("/health")
def health_check():
    """
    서버가 정상적으로 작동하는지 확인하는 API입니다.
    """
    return {"status": "OK", "message": "Daily Question Service is running."}

@app.get("/")
def root():
    return {"message": "Welcome to Daily Question Service"}
