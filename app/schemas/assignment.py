from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AssignmentBase(BaseModel):
    title: str
    description: str
    due_date: datetime

class AssignmentCreate(AssignmentBase):
    course_id: int

class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None

class Assignment(AssignmentBase):
    id: int
    course_id: int
    created_at: datetime

    class Config:
        from_attributes = True