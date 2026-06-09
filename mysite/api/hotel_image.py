from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import HotelImage
from mysite.database.schema import HotelImageInputSchema, HotelImageOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

hotel_image_router = APIRouter(prefix='/hotel_image', tags=['HotelImage'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@hotel_image_router.post('/', response_model=HotelImageOutSchema)
async def hotel_image_create(user: HotelImageInputSchema, db: Session = Depends(get_db)):
    user_db = HotelImage(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@hotel_image_router.get('/', response_model=List[HotelImageOutSchema])
async def hotel_image_list(db: Session = Depends(get_db)):
    return db.query(HotelImage).all()



@hotel_image_router.get('/{hotel_image_id}/', response_model=HotelImageOutSchema)
async def hotel_image_detail(user_id: int, db: Session = Depends(get_db)):
    user = db.query(HotelImage).filter(HotelImage.id==user_id).first()
    if not user:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return user


@hotel_image_router.put('/{hotel_image_id}/', response_model=dict)
async def hotel_image_update(user_id: int, user: HotelImageInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(HotelImage).filter(HotelImage.id==user_id).first()
    if not user_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for user_key, user_value in user.dict().items():
        setattr(user_db, user_key, user_value)


    db.commit()
    db.refresh(user_db)
    return {'message': 'Маалымат озгорулду'}


@hotel_image_router.delete('/{hotel_image_id}/', response_model=dict)
async def hotel_image_delete(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(HotelImage).filter(HotelImage.id==user_id).first()
    if not user_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(user_db)
    db.commit()
    return {'massage': 'Маалымат удaлить болду'}


