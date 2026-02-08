from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StudyMaterialBase(BaseModel):
    title: str
    description: str
    file_url: str

class StudyMaterialCreate(StudyMaterialBase):
    course_id: int
    uploaded_by: int

class StudyMaterialUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    file_url: Optional[str] = None

class StudyMaterial(StudyMaterialBase):
    id: int
    course_id: int
    uploaded_by: int
    created_at: datetime

    class Config:
        from_attributes = True