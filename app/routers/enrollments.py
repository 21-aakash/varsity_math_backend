from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.config.database import get_db
from app.models.enrollment import Enrollment
from app.schemas.enrollment import Enrollment as EnrollmentSchema, EnrollmentCreate, EnrollmentUpdate
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=list[EnrollmentSchema])
async def read_enrollments(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role not in ["faculty", "admin"]:
        # Students can only see their own enrollments
        query = select(Enrollment).where(Enrollment.user_id == current_user.id)
    else:
        # Faculty/admin can see all
        query = select(Enrollment)
    result = await db.execute(query)
    enrollments = result.scalars().all()
    return enrollments

@router.post("/", response_model=EnrollmentSchema)
async def create_enrollment(enrollment: EnrollmentCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_enrollment = Enrollment(**enrollment.dict(), user_id=current_user.id)
    db.add(db_enrollment)
    await db.commit()
    await db.refresh(db_enrollment)
    return db_enrollment

@router.get("/{enrollment_id}", response_model=EnrollmentSchema)
async def read_enrollment(enrollment_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    enrollment = await db.get(Enrollment, enrollment_id)
    if enrollment is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    if current_user.role not in ["faculty", "admin"] and enrollment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return enrollment

@router.put("/{enrollment_id}", response_model=EnrollmentSchema)
async def update_enrollment(enrollment_id: int, enrollment_update: EnrollmentUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    enrollment = await db.get(Enrollment, enrollment_id)
    if enrollment is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    if current_user.role not in ["faculty", "admin"] and enrollment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    for field, value in enrollment_update.dict(exclude_unset=True).items():
        setattr(enrollment, field, value)
    await db.commit()
    await db.refresh(enrollment)
    return enrollment