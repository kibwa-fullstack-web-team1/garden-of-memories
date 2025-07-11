from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class StoryBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None

class StoryCreate(StoryBase):
    pass

class StoryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None

class StoryInDB(StoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# StorySegment 관련 스키마
class StorySegmentBase(BaseModel):
    order: int
    segment_text: str

class StorySegmentCreate(StorySegmentBase):
    pass

class StorySegmentInDB(StorySegmentBase):
    id: int
    story_id: int

    class Config:
        orm_mode = True

class StorySegmentResponse(StorySegmentInDB):
    pass

class StoryResponse(StoryInDB):
    segments: List[StorySegmentResponse] = [] 