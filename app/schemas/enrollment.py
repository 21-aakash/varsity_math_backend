from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EnrollmentBase(BaseModel):
    course_id: int
    first_name: str
    last_name: str
    phone: str
    payment_method: str
    payment_screenshot_url: Optional[str] = None
    profile_image_url: Optional[str] = None

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentUpdate(BaseModel):
    status: Optional[str] = None
    payment_screenshot_url: Optional[str] = None
    profile_image_url: Optional[str] = None

class Enrollment(EnrollmentBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True