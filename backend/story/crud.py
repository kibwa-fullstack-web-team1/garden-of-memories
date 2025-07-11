import os
import openai
from sqlalchemy.orm import Session, joinedload
import models
import schemas
from typing import List, Optional
import json
import re

def split_story_with_openai(content: str) -> List[str]:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = (
        "아래 이야기를 순서대로 문장 단위로 나눠서 리스트(JSON array)로 만들어줘. "
        "각 문장은 따옴표로 감싸고, 리스트 형태로만 답변해줘.\n\n"
        f"{content}"
    )
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "너는 문장 분리기야."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024,
        temperature=0.2,
    )
    text = response.choices[0].message.content
    match = re.search(r"\[.*\]", text if text is not None else "", re.DOTALL)
    if match:
        return json.loads(match.group(0))
    else:
        return [s.strip() for s in content.split('.') if s.strip()]

def create_story(db: Session, story_create: schemas.StoryCreate) -> models.Story:
    db_story = models.Story(**story_create.dict())
    db.add(db_story)
    db.commit()
    db.refresh(db_story)

    # OpenAI API로 이야기 분리
    segments = split_story_with_openai(str(db_story.content))
    for idx, seg in enumerate(segments, start=1):
        db_segment = models.StorySegment(
            story_id=db_story.id,
            order=idx,
            segment_text=seg
        )
        db.add(db_segment)
    db.commit()
    db.refresh(db_story)
    return db_story

def get_story(db: Session, story_id: int) -> Optional[models.Story]:
    return db.query(models.Story).options(joinedload(models.Story.segments)).filter(models.Story.id == story_id).first()

def get_stories(db: Session, skip: int = 0, limit: int = 100) -> List[models.Story]:
    return db.query(models.Story).options(joinedload(models.Story.segments)).offset(skip).limit(limit).all()

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