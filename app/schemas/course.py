from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CourseBase(BaseModel):
    title: str
    description: str

class CourseCreate(CourseBase):
    instructor_id: int

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class Course(CourseBase):
    id: int
    instructor_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True