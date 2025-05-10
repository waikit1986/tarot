from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from database import SessionLocal
from . import models_profile, schemas_profile

router = APIRouter(prefix="/profiles", tags=["Profiles"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas_profile.ProfileOut)
def create_profile(profile: schemas_profile.ProfileCreate, db: Session = Depends(get_db)):
    new_profile = models_profile.Profile(
        user_name=profile.user_name,
        age=profile.age,
        bio=profile.bio
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

@router.get("/{profile_id}", response_model=schemas_profile.ProfileOut)
def get_profile(profile_id: UUID, db: Session = Depends(get_db)):
    profile = db.query(models_profile.Profile).filter(models_profile.Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.patch("/{profile_id}", response_model=schemas_profile.ProfileOut)
def update_profile(profile_id: UUID, updates: schemas_profile.ProfileUpdate, db: Session = Depends(get_db)):
    profile = db.query(models_profile.Profile).filter(models_profile.Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    if updates.user_name is not None:
        profile.user_name = updates.user_name
    if updates.age is not None:
        profile.age = updates.age
    if updates.bio is not None:
        profile.bio = updates.bio

    db.commit()
    db.refresh(profile)
    return profile

@router.delete("/{profile_id}", response_model=schemas_profile.ProfileDeleted)
def delete_profile(profile_id: UUID, db: Session = Depends(get_db)):
    profile = db.query(models_profile.Profile).filter(models_profile.Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    db.delete(profile)
    db.commit()
    return {"id": profile_id}
