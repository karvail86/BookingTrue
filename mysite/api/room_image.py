from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import RoomImage
from mysite.database.schema import RoomImageInputSchema, RoomImageOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

room_image_router = APIRouter(prefix='/room_image', tags=['RoomImage'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@room_image_router.post('/', response_model=RoomImageOutSchema)
async def room_image_create(room_image: RoomImageInputSchema, db: Session = Depends(get_db)):
    room_image_db = RoomImage(**room_image.dict())
    db.add(room_image_db)
    db.commit()
    db.refresh(room_image_db)
    return room_image_db


@room_image_router.get('/', response_model=List[RoomImageOutSchema])
async def room_image_list(db: Session = Depends(get_db)):
    return db.query(RoomImage).all()



@room_image_router.get('/{room_image_id}/', response_model=RoomImageOutSchema)
async def room_image_detail(room_image_id: int, db: Session = Depends(get_db)):
    room_image = db.query(RoomImage).filter(RoomImage.id==room_image_id).first()
    if not room_image:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return room_image


@room_image_router.put('/room_image_id}/', response_model=dict)
async def room_update(room_image_id: int, room_image: RoomImageInputSchema, db: Session = Depends(get_db)):
    room_image_db = db.query(RoomImage).filter(RoomImage.id==room_image_id).first()
    if not room_image_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for room_image_key, room_image_value in room_image.dict().items():
        setattr(room_image_db, room_image_key,room_image_value)


    db.commit()
    db.refresh(room_image_db)
    return {'message': 'Маалымат озгорулду'}


@room_image_router.delete('/room_image_id}/', response_model=dict)
async def room_image_delete(room_image_id: int, db: Session = Depends(get_db)):
    room_image_db = db.query(RoomImage).filter(RoomImage.id==room_image_id).first()
    if not room_image_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(room_image_db)
    db.commit()
    return {'massage': 'Маалымат удaлить болду'}


