from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QuizBase(BaseModel):
    title: str
    description: str

class QuizCreate(QuizBase):
    course_id: int

class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class Quiz(QuizBase):
    id: int
    course_id: int
    created_at: datetime

    class Config:
        from_attributes = True