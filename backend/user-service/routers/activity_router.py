from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from database import SessionLocal

router = APIRouter(
    prefix="/activity",
    tags=["Activities"],
)

# DB 세션을 가져오는 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 활동 유형(ActivityType) API
@router.post("/types/", response_model=schemas.ActivityType)
def create_activity_type(activity_type: schemas.ActivityTypeCreate, db: Session = Depends(get_db)):
    db_activity_type = models.ActivityType(**activity_type.model_dump())
    db.add(db_activity_type)
    db.commit()
    db.refresh(db_activity_type)
    return db_activity_type

@router.get("/types/", response_model=List[schemas.ActivityType])
def read_activity_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    activity_types = db.query(models.ActivityType).offset(skip).limit(limit).all()
    return activity_types

# 활동 로그(ActivityLog) API
@router.post("/logs/", response_model=schemas.ActivityLog)
def create_activity_log(activity_log: schemas.ActivityLogCreate, db: Session = Depends(get_db)):
    # 사용자 존재 여부 확인
    db_user = db.query(models.User).filter(models.User.id == activity_log.user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 활동 유형 존재 여부 확인
    db_activity_type = db.query(models.ActivityType).filter(models.ActivityType.id == activity_log.activity_type_id).first()
    if db_activity_type is None:
        raise HTTPException(status_code=404, detail="ActivityType not found")

    db_activity_log = models.ActivityLog(**activity_log.model_dump())
    db.add(db_activity_log)
    db.commit()
    db.refresh(db_activity_log)
    return db_activity_log

@router.get("/logs/user/{user_id}", response_model=List[schemas.ActivityLogWithDetails])
def read_activity_logs_by_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # 사용자 존재 여부 확인
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    activity_logs = db.query(models.ActivityLog).filter(models.ActivityLog.user_id == user_id).offset(skip).limit(limit).all()
    return activity_logs
