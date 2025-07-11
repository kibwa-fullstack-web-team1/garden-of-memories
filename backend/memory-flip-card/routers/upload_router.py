from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import os
import models, schemas
from database import SessionLocal
from dotenv import load_dotenv

import boto3
import uuid
from datetime import datetime
from fastapi import File, UploadFile, Form
from fastapi.responses import JSONResponse

from models.upload_photo import FamilyPhoto

load_dotenv()

router = APIRouter()

# S3 설정
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
AWS_S3_REGION = os.getenv("AWS_S3_REGION")


s3_client = boto3.client(
    "s3",
    region_name=AWS_S3_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# DB 세션을 가져오는 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# S3 업로드 함수
def upload_to_s3(file: UploadFile, user_id: str) -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    unique_filename = f"{user_id}_{timestamp}_{uuid.uuid4().hex}_{file.filename}"
    s3_key = f"family_photos/{unique_filename}"

    # S3에 파일 업로드
    s3_client.upload_fileobj(
        file.file,
        AWS_S3_BUCKET_NAME,
        s3_key,
        # ExtraArgs={"ACL": "public-read", "ContentType": file.content_type}
    )

    file_url = f"https://{AWS_S3_BUCKET_NAME}.s3.{AWS_S3_REGION}.amazonaws.com/{s3_key}"
    return file_url

@router.post("/upload-family-photo")
async def upload_family_photo(
    user_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 유효성 검사
    if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        raise HTTPException(status_code=400, detail="이미지 파일만 허용됩니다.")

    # S3 업로드
    try:
        s3_url = upload_to_s3(file, user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"S3 업로드 실패: {str(e)}")

    # DB 저장
    photo_record = FamilyPhoto(
        user_id=user_id,
        file_path=s3_url
    )
    db.add(photo_record)
    db.commit()
    db.refresh(photo_record)

    return JSONResponse(status_code=200, content={
    "message": "업로드 성공",
    "photo_id": photo_record.id,
    "file_url": s3_url
})

# +) 업로드 파일 용량 제한