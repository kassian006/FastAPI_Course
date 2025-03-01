from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from course_app.db.models import Course
from course_app.db.schema import CourseSchema
from course_app.db.database import SessionLocal

course_router = APIRouter(prefix="/course", tags=["Courses"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@course_router.post('/course/create/', response_model=CourseSchema)
async def create_course(course: CourseSchema, db: Session = Depends(get_db)):
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@course_router.get('/course/', response_model=List[CourseSchema])
async def list_course(db: Session = Depends(get_db)):
    return db.query(Course).all()


@course_router.get('/course/{course_id}/', response_model=CourseSchema)
async def detail_course(course_id: int, db:Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id==course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    return course


@course_router.put('/course/{course_id}/', response_model=CourseSchema)
async def update_course(course_id: int,
                        course_data: CourseSchema,
                        db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id==course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    for course_key, course_value in course_data.dict().items():
        setattr(course, course_key, course_value)
    db.commit()
    db.refresh(course)
    return course


@course_router.delete('/course/{course_id}')
async def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id==course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    db.delete(course)
    db.commit()
    return {'message': 'This Course is Deleted'}

