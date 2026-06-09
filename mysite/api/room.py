from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Room
from mysite.database.schema import RoomInputSchema, RoomOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

room_router = APIRouter(prefix='/room', tags=['Room'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@room_router.post('/', response_model=RoomOutSchema)
async def room_create(user: RoomInputSchema, db: Session = Depends(get_db)):
    user_db = Room(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@room_router.get('/', response_model=List[RoomOutSchema])
async def room_list(db: Session = Depends(get_db)):
    return db.query(Room).all()



@room_router.get('/{room_id}/', response_model=RoomOutSchema)
async def room_detail(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Room).filter(Room.id==user_id).first()
    if not user:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return user


@room_router.put('/{room_id}/', response_model=dict)
async def room_update(user_id: int, user: RoomInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(Room).filter(Room.id==user_id).first()
    if not user_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for user_key, user_value in user.dict().items():
        setattr(user_db, user_key, user_value)


    db.commit()
    db.refresh(user_db)
    return {'message': 'Маалымат озгорулду'}


@room_router.delete('/{room_id}/', response_model=dict)
async def room_delete(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(Room).filter(Room.id==user_id).first()
    if not user_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(user_db)
    db.commit()
    return {'massage': 'Маалымат удaлить болду'}


