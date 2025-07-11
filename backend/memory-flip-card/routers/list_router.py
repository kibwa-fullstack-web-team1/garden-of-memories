from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from models.upload_photo import FamilyPhoto
from schemas.photo_schema import FamilyPhotoListResponse, PhotoItem

router = APIRouter()

# DB 세션을 가져오는 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#가족사진 목록 조회 API
@router.get("/photo-list", response_model=FamilyPhotoListResponse)
def get_family_photos(user_id: str = Query(...), db: Session = Depends(get_db)):
    photos = db.query(FamilyPhoto).filter(FamilyPhoto.user_id == user_id).all()

    if not photos:
        raise HTTPException(status_code=404, detail="등록된 가족사진이 없습니다.")

    return FamilyPhotoListResponse(
        user_id=user_id,
        photos=[PhotoItem(id=photo.id, file_url=photo.file_path) for photo in photos]
    )