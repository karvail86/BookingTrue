from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Booking
from mysite.database.schema import BookingInputSchema, BookingOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

booking_router = APIRouter(prefix='/booking', tags=['Booking'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@booking_router.post('/', response_model=BookingOutSchema)
async def booking_create(user: BookingInputSchema, db: Session = Depends(get_db)):
    user_db = Booking(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@booking_router.get('/', response_model=List[BookingOutSchema])
async def booking_list(db: Session = Depends(get_db)):
    return db.query(Booking).all()



@booking_router.get('/{booking_id}/', response_model=BookingOutSchema)
async def booking_detail(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Booking).filter(Booking.id==user_id).first()
    if not user:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return user


@booking_router.put('/{booking_id}/', response_model=dict)
async def booking_update(user_id: int, user: BookingInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(Booking).filter(Booking.id==user_id).first()
    if not user_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for user_key, user_value in user.dict().items():
        setattr(user_db, user_key, user_value)


    db.commit()
    db.refresh(user_db)
    return {'message': 'Маалымат озгорулду'}


@booking_router.delete('/{booking_id}/', response_model=dict)
async def booking_delete(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(Booking).filter(Booking.id==user_id).first()
    if not user_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(user_db)
    db.commit()
    return {'massage': 'Маалымат удaлить болду'}


