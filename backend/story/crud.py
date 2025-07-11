from sqlalchemy.orm import Session
import models
import schemas
from typing import List, Optional

def create_story(db: Session, story_create: schemas.StoryCreate) -> models.Story:
    db_story = models.Story(**story_create.dict())
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    return db_story

def get_story(db: Session, story_id: int) -> Optional[models.Story]:
    return db.query(models.Story).filter(models.Story.id == story_id).first()

def get_stories(db: Session, skip: int = 0, limit: int = 100) -> List[models.Story]:
    return db.query(models.Story).offset(skip).limit(limit).all()

def update_story(db: Session, story_id: int, story_update: schemas.StoryUpdate) -> Optional[models.Story]:
    story = db.query(models.Story).filter(models.Story.id == story_id).first()
    if not story:
        return None
    for key, value in story_update.dict(exclude_unset=True).items():
        setattr(story, key, value)
    db.commit()
    db.refresh(story)
    return story

def delete_story(db: Session, story_id: int) -> bool:
    story = db.query(models.Story).filter(models.Story.id == story_id).first()
    if not story:
        return False
    db.delete(story)
    db.commit()
    return True 