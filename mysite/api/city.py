from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import City
from mysite.database.schema import CityInputSchema, CityOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

city_router = APIRouter(prefix='/city', tags=['City'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@city_router.post('/', response_model=CityOutSchema)
async def city_create(user: CityInputSchema, db: Session = Depends(get_db)):
    user_db = City(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@city_router.get('/', response_model=List[CityOutSchema])
async def city_list(db: Session = Depends(get_db)):
    return db.query(City).all()



@city_router.get('/{city_id}/', response_model=CityOutSchema)
async def city_detail(user_id: int, db: Session = Depends(get_db)):
    user = db.query(City).filter(City.id==user_id).first()
    if not user:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return user


@city_router.put('/{city_id}/', response_model=dict)
async def city_update(user_id: int, user: CityInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(City).filter(City.id==user_id).first()
    if not user_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for user_key, user_value in user.dict().items():
        setattr(user_db, user_key, user_value)


    db.commit()
    db.refresh(user_db)
    return {'message': 'Маалымат озгорулду'}


@city_router.delete('/{city_id}/', response_model=dict)
async def city_delete(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(City).filter(City.id==user_id).first()
    if not user_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(user_db)
    db.commit()
    return {'massage': 'Маалымат удaлить болду'}


