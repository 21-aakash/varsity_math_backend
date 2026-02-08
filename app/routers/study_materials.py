from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.config.database import get_db
from app.models.study_material import StudyMaterial
from app.schemas.study_material import StudyMaterial as StudyMaterialSchema, StudyMaterialCreate, StudyMaterialUpdate
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=list[StudyMaterialSchema])
async def read_study_materials(course_id: int = None, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    query = select(StudyMaterial)
    if course_id:
        query = query.where(StudyMaterial.course_id == course_id)
    result = await db.execute(query.offset(skip).limit(limit))
    materials = result.scalars().all()
    return materials

@router.post("/", response_model=StudyMaterialSchema)
async def create_study_material(material: StudyMaterialCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role not in ["faculty", "admin"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_material = StudyMaterial(**material.dict())
    db.add(db_material)
    await db.commit()
    await db.refresh(db_material)
    return db_material

@router.get("/{material_id}", response_model=StudyMaterialSchema)
async def read_study_material(material_id: int, db: AsyncSession = Depends(get_db)):
    material = await db.get(StudyMaterial, material_id)
    if material is None:
        raise HTTPException(status_code=404, detail="Study material not found")
    return material

@router.put("/{material_id}", response_model=StudyMaterialSchema)
async def update_study_material(material_id: int, material_update: StudyMaterialUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    material = await db.get(StudyMaterial, material_id)
    if material is None:
        raise HTTPException(status_code=404, detail="Study material not found")
    if current_user.role not in ["faculty", "admin"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    for field, value in material_update.dict(exclude_unset=True).items():
        setattr(material, field, value)
    await db.commit()
    await db.refresh(material)
    return material