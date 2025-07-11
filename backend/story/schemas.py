from pydantic import BaseModel
from typing import Optional
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

class StoryResponse(StoryInDB):
    pass 