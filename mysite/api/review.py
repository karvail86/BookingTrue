from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Review
from mysite.database.schema import ReviewInputSchema, ReviewOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

review_router = APIRouter(prefix='/review', tags=['Review'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@review_router.post('/', response_model=ReviewOutSchema)
async def review_create(user: ReviewInputSchema, db: Session = Depends(get_db)):
    user_db = Review(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@review_router.get('/', response_model=List[ReviewOutSchema])
async def review_list(db: Session = Depends(get_db)):
    return db.query(Review).all()



@review_router.get('/{review_id}/', response_model=ReviewOutSchema)
async def review_detail(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Review).filter(Review.id==user_id).first()
    if not user:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return user


@review_router.put('/{review_id}/', response_model=dict)
async def review_update(user_id: int, user: ReviewInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(Review).filter(Review.id==user_id).first()
    if not user_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for user_key, user_value in user.dict().items():
        setattr(user_db, user_key, user_value)


    db.commit()
    db.refresh(user_db)
    return {'message': 'Маалымат озгорулду'}


@review_router.delete('/{review_id}/', response_model=dict)
async def review_delete(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(Review).filter(Review.id==user_id).first()
    if not user_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(user_db)
    db.commit()
    return {'massage': 'Маалымат удaлить болду'}


