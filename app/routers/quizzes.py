from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.config.database import get_db
from app.models.quiz import Quiz
from app.schemas.quiz import Quiz as QuizSchema, QuizCreate, QuizUpdate
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=list[QuizSchema])
async def read_quizzes(course_id: int = None, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    query = select(Quiz)
    if course_id:
        query = query.where(Quiz.course_id == course_id)
    result = await db.execute(query.offset(skip).limit(limit))
    quizzes = result.scalars().all()
    return quizzes

@router.post("/", response_model=QuizSchema)
async def create_quiz(quiz: QuizCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role not in ["faculty", "admin"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_quiz = Quiz(**quiz.dict())
    db.add(db_quiz)
    await db.commit()
    await db.refresh(db_quiz)
    return db_quiz

@router.get("/{quiz_id}", response_model=QuizSchema)
async def read_quiz(quiz_id: int, db: AsyncSession = Depends(get_db)):
    quiz = await db.get(Quiz, quiz_id)
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@router.put("/{quiz_id}", response_model=QuizSchema)
async def update_quiz(quiz_id: int, quiz_update: QuizUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    quiz = await db.get(Quiz, quiz_id)
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    if current_user.role not in ["faculty", "admin"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    for field, value in quiz_update.dict(exclude_unset=True).items():
        setattr(quiz, field, value)
    await db.commit()
    await db.refresh(quiz)
    return quiz