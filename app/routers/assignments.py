from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.config.database import get_db
from app.models.assignment import Assignment
from app.schemas.assignment import Assignment as AssignmentSchema, AssignmentCreate, AssignmentUpdate
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=list[AssignmentSchema])
async def read_assignments(course_id: int = None, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    query = select(Assignment)
    if course_id:
        query = query.where(Assignment.course_id == course_id)
    result = await db.execute(query.offset(skip).limit(limit))
    assignments = result.scalars().all()
    return assignments

@router.post("/", response_model=AssignmentSchema)
async def create_assignment(assignment: AssignmentCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role not in ["faculty", "admin"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_assignment = Assignment(**assignment.dict())
    db.add(db_assignment)
    await db.commit()
    await db.refresh(db_assignment)
    return db_assignment

@router.get("/{assignment_id}", response_model=AssignmentSchema)
async def read_assignment(assignment_id: int, db: AsyncSession = Depends(get_db)):
    assignment = await db.get(Assignment, assignment_id)
    if assignment is None:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment

@router.put("/{assignment_id}", response_model=AssignmentSchema)
async def update_assignment(assignment_id: int, assignment_update: AssignmentUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    assignment = await db.get(Assignment, assignment_id)
    if assignment is None:
        raise HTTPException(status_code=404, detail="Assignment not found")
    if current_user.role not in ["faculty", "admin"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    for field, value in assignment_update.dict(exclude_unset=True).items():
        setattr(assignment, field, value)
    await db.commit()
    await db.refresh(assignment)
    return assignment