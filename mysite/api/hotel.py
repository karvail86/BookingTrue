from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Hotel
from mysite.database.schema import HotelInputSchema, HotelOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

hotel_router = APIRouter(prefix='/hotel', tags=['Hotel'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@hotel_router.post('/', response_model=HotelOutSchema)
async def hotel_create(user: HotelInputSchema, db: Session = Depends(get_db)):
    user_db = Hotel(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@hotel_router.get('/', response_model=List[HotelOutSchema])
async def hotel_list(db: Session = Depends(get_db)):
    return db.query(Hotel).all()



@hotel_router.get('/{hotel_id}/', response_model=HotelOutSchema)
async def hotel_detail(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Hotel).filter(Hotel.id==user_id).first()
    if not user:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return user


@hotel_router.put('/{hotel_id}/', response_model=dict)
async def hotel_update(user_id: int, user: HotelInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(Hotel).filter(Hotel.id==user_id).first()
    if not user_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for user_key, user_value in user.dict().items():
        setattr(user_db, user_key, user_value)


    db.commit()
    db.refresh(user_db)
    return {'message': 'Маалымат озгорулду'}


@hotel_router.delete('/{hotel_id}/', response_model=dict)
async def hotel_delete(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(Hotel).filter(Hotel.id==user_id).first()
    if not user_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(user_db)
    db.commit()
    return {'massage': 'Маалымат удaлить болду'}


