from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import crud
from database import get_db

router = APIRouter(
    prefix="/stories",
    tags=["stories"]
)

@router.post("/", response_model=schemas.StoryResponse, status_code=status.HTTP_201_CREATED)
def create_story(story: schemas.StoryCreate, db: Session = Depends(get_db)):
    return crud.create_story(db, story)

@router.get("/", response_model=List[schemas.StoryResponse])
def read_stories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_stories(db, skip=skip, limit=limit)

@router.get("/{story_id}", response_model=schemas.StoryResponse)
def read_story(story_id: int, db: Session = Depends(get_db)):
    story = crud.get_story(db, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story

@router.put("/{story_id}", response_model=schemas.StoryResponse)
def update_story(story_id: int, story_update: schemas.StoryUpdate, db: Session = Depends(get_db)):
    story = crud.update_story(db, story_id, story_update)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story

@router.delete("/{story_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_story(story_id: int, db: Session = Depends(get_db)):
    success = crud.delete_story(db, story_id)
    if not success:
        raise HTTPException(status_code=404, detail="Story not found")
    return None 