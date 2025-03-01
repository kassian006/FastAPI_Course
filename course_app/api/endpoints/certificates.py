from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from course_app.db.models import Certificate
from course_app.db.schema import CertificateSchema
from course_app.db.database import SessionLocal

certificate_router = APIRouter(prefix="/certificate", tags=["Certificates"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@certificate_router.post('/certificate/create/', response_model=CertificateSchema)
async def create_certificate(certificate: CertificateSchema, db: Session = Depends(get_db)):
    db_certificate = Certificate(**certificate.dict())
    db.add(db_certificate)
    db.commit()
    db.refresh(db_certificate)
    return db_certificate


@certificate_router.get('/certificate/', response_model=List[CertificateSchema])
async def list_certificate(db: Session = Depends(get_db)):
    return db.query(Certificate).all()


@certificate_router.get('/certificate/{certificate_id}/', response_model=CertificateSchema)
async def detail_certificate(certificate_id: int, db:Session = Depends(get_db)):
    certificate = db.query(Certificate).filter(Certificate.id==certificate_id).first()
    if certificate is None:
        raise HTTPException(status_code=404, detail='Certificate not found')
    return certificate


@certificate_router.put('/certificate/{certificate_id}/', response_model=CertificateSchema)
async def update_certificate(certificate_id: int,
                        certificate_data: CertificateSchema,
                        db: Session = Depends(get_db)):
    certificate = db.query(Certificate).filter(Certificate.id==certificate_id).first()
    if certificate is None:
        raise HTTPException(status_code=404, detail='Certificate not found')
    for certificate_key, certificate_value in certificate_data.dict().items():
        setattr(certificate, certificate_key, certificate_value)
    db.commit()
    db.refresh(certificate)
    return certificate


@certificate_router.delete('/certificate/{certificate_id}')
async def delete_certificate(certificate_id: int, db: Session = Depends(get_db)):
    certificate = db.query(Certificate).filter(Certificate.id==certificate_id).first()
    if certificate is None:
        raise HTTPException(status_code=404, detail='Certificate not found')
    db.delete(certificate)
    db.commit()
    return {'message': 'This Certificate is Deleted'}
