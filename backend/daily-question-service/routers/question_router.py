from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from schemas import question_schema
from models import question as question_model
from database import get_db

router = APIRouter(
    prefix="/questions",
    tags=["Questions"]
)

@router.post("/", response_model=question_schema.Question)
def create_question(question: question_schema.QuestionCreate, db: Session = Depends(get_db)):
    db_question = question_model.Question(content=question.content)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@router.get("/", response_model=List[question_schema.Question])
def read_questions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    questions = db.query(question_model.Question).offset(skip).limit(limit).all()
    return questions

@router.get("/{question_id}", response_model=question_schema.Question)
def read_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(question_model.Question).filter(question_model.Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.put("/{question_id}", response_model=question_schema.Question)
def update_question(question_id: int, question: question_schema.QuestionCreate, db: Session = Depends(get_db)):
    db_question = db.query(question_model.Question).filter(question_model.Question.id == question_id).first()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    db_question.content = question.content
    db.commit()
    db.refresh(db_question)
    return db_question

@router.delete("/{question_id}", response_model=question_schema.Question)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    db_question = db.query(question_model.Question).filter(question_model.Question.id == question_id).first()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(db_question)
    db.commit()
    return db_question

@router.get("/daily", response_model=question_schema.Question)
def get_daily_question(db: Session = Depends(get_db)):
    """
    LLM을 연동하여 사용자에게 개인화된 '오늘의 질문'을 추천합니다.
    현재는 임시로 첫 번째 질문을 반환합니다.
    """
    # TODO: LLM 연동 로직 구현 (사용자 메타데이터/활동 기반 질문 생성)
    # 현재는 데이터베이스에서 첫 번째 질문을 가져오는 것으로 대체합니다.
    question = db.query(question_model.Question).first()
    if not question:
        raise HTTPException(status_code=404, detail="No questions available")
    return question
