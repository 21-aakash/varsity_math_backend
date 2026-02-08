from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.config.database import get_db
from app.models.course import Course
from app.schemas.course import Course as CourseSchema, CourseCreate, CourseUpdate
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=list[CourseSchema])
async def read_courses(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).offset(skip).limit(limit))
    courses = result.scalars().all()
    return courses

@router.post("/", response_model=CourseSchema)
async def create_course(course: CourseCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role not in ["faculty", "admin"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_course = Course(**course.dict())
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course

@router.get("/{course_id}", response_model=CourseSchema)
async def read_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.put("/{course_id}", response_model=CourseSchema)
async def update_course(course_id: int, course_update: CourseUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    if current_user.role not in ["faculty", "admin"] and course.instructor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    for field, value in course_update.dict(exclude_unset=True).items():
        setattr(course, field, value)
    await db.commit()
    await db.refresh(course)
    return course