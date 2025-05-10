from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from . import models_profile, schemas_profile
from database import SessionLocal

router = APIRouter(prefix="/profiles", tags=["Profiles"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas_profile.ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(profile: schemas_profile.ProfileCreate, db: Session = Depends(get_db)):
    db_profile = models_profile.Profile(**profile.model_dump())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.get("/{profile_id}", response_model=schemas_profile.ProfileResponse)
def get_profile(profile_id: UUID, db: Session = Depends(get_db)):
    profile = db.query(models_profile.Profile).filter(models_profile.Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile

@router.get("/", response_model=List[schemas_profile.ProfileResponse])
def get_all_profiles(db: Session = Depends(get_db)):
    profiles = db.query(models_profile.Profile).all()
    return profiles

@router.patch("/{profile_id}", response_model=schemas_profile.ProfileResponse)
def update_profile(
    profile_id: UUID,
    updates: schemas_profile.ProfileUpdate,
    db: Session = Depends(get_db)
):
    db_profile = db.query(models_profile.Profile).filter(models_profile.Profile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    
    update_data = updates.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_profile, field, value)
    
    db_profile.updated_at = datetime.now()
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.delete("/{profile_id}", response_model=schemas_profile.ProfileDeleteResponse)
def delete_profile(profile_id: UUID, db: Session = Depends(get_db)):
    profile = db.query(models_profile.Profile).filter(models_profile.Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    
    db.delete(profile)
    db.commit()
    
    return {
        "id": profile_id,
        "message": "Profile deleted successfully",
        "deleted_at": datetime.now()
    }