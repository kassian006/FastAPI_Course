from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from course_app.db.models import Exam
from course_app.db.schema import ExamSchema
from course_app.db.database import SessionLocal

exam_router = APIRouter(prefix="/exam", tags=["Exams"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@exam_router.post('/exam/create/', response_model=ExamSchema)
async def create_exam(exam: ExamSchema, db: Session = Depends(get_db)):
    db_exam = Exam(**exam.dict())
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    return db_exam


@exam_router.get('/exam/', response_model=List[ExamSchema])
async def list_exam(db: Session = Depends(get_db)):
    return db.query(Exam).all()


@exam_router.get('/exam/{exam_id}/', response_model=ExamSchema)
async def detail_exam(exam_id: int, db:Session = Depends(get_db)):
    exam = db.query(Exam).filter(Exam.id==exam_id).first()
    if exam is None:
        raise HTTPException(status_code=404, detail='Exam not found')
    return exam


@exam_router.put('/exam/{exam_id}/', response_model=ExamSchema)
async def update_exam(exam_id: int,
                        exam_data: ExamSchema,
                        db: Session = Depends(get_db)):
    exam = db.query(Exam).filter(Exam.id==exam_id).first()
    if exam is None:
        raise HTTPException(status_code=404, detail='Exam not found')
    for exam_key, exam_value in exam_data.dict().items():
        setattr(exam, exam_key, exam_value)
    db.commit()
    db.refresh(exam)
    return exam


@exam_router.delete('/exam/{exam_id}')
async def delete_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(Exam).filter(Exam.id==exam_id).first()
    if exam is None:
        raise HTTPException(status_code=404, detail='Exam not found')
    db.delete(exam)
    db.commit()
    return {'message': 'This Exam is Deleted'}
