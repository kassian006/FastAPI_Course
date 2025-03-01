from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from course_app.db.models import UserProfile
from course_app.db.schema import UserProfileSchema
from course_app.db.database import SessionLocal

user_router = APIRouter(prefix="/user", tags=["Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.post('/create/', response_model=UserProfileSchema)
async def register(user: UserProfileSchema, db: Session = Depends(get_db)):
    existing_user = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail= 'Username бар экен')

    new_user = UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        phone_number=user.phone_number,
        age=user.age,
        profile_picture=user.profile_picture,
        role=user.role,
        hashed_password=user.password

    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@user_router.get('/', response_model=List[UserProfileSchema])
async def list_users(db:Session = Depends(get_db)):
    return db.query(UserProfile).all()


@user_router.get('/{user_id}/', response_model=UserProfileSchema)
async def detail_user(user_id: int, db:Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id==user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@user_router.put('/{user_id}/', response_model=UserProfileSchema)
async def update_user(user_id: int,
                          user_data: UserProfileSchema,
                          db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='Category not found')

    user.first_name = user_data.first_name
    user.last_name = user_data.last_name
    user.username = user_data.username
    user.phone_number = user_data.phone_number
    user.age = user_data.age
    user_data.profile_picture = user_data.profile_picture
    user.role = user_data.role
    db.commit()
    db.refresh(user)
    return user


@user_router.delete('/{user_id}/', response_model=UserProfileSchema)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
