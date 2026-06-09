from pydantic import BaseModel, EmailStr
from typing import Optional
from .models import RoleChoices, RoomTypeChoices
from datetime import date, datetime


class UserProfileSchema(BaseModel):
    id: int
    username: str
    email: EmailStr

class Login(BaseModel):
    username: str
    password: str



class UserProfileInputSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    age: Optional[int]
    user_img: str
    country: Optional[int]
    phone_number: Optional[str]



class UserProfileOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    age: Optional[int]
    user_img: str
    country: Optional[int]
    phone_number: Optional[str]
    user_role: RoleChoices
    register_date: date


class CityInputSchema(BaseModel):
    city_image: str
    city_name: str

class CityOutSchema(BaseModel):
    id: int
    city_image: str
    city_name: str



class ServiceInputSchema(BaseModel):
    service_image: str
    service_name: str


class ServiceOutSchema(BaseModel):
    id: int
    service_image: str
    service_name: str




class HotelInputSchema(BaseModel):
    hotel_name: str
    city_id: int
    country: int
    street: str
    postal_code: int
    hotel_stars: int
    description: str
    service_id: int


class HotelOutSchema(BaseModel):
    id: int
    hotel_name: str
    city_id: int
    country: int
    street: str
    postal_code: int
    hotel_stars: int
    description: str
    service_id: int



class HotelImageInputSchema(BaseModel):
    hotel_id: int
    hotel_image: str


class HotelImageOutSchema(BaseModel):
    id: int
    hotel_id: int
    hotel_image: str



class RoomInputSchema(BaseModel):
    hotel_id: int
    room_number: int
    price: int
    room_type: RoomTypeChoices
    description: str



class RoomOutSchema(BaseModel):
    id: int
    hotel_id: int
    room_number: int
    price: int
    room_type: RoomTypeChoices
    description: str




class RoomImageInputSchema(BaseModel):
    room_id: int
    room_image: str


class RoomImageOutSchema(BaseModel):
    id: int
    room_id: int
    room_image: str




class ReviewInputSchema(BaseModel):
    user_id: int
    hotel_id: int
    rating: int
    comment: str
    created_date: date


class ReviewOutSchema(BaseModel):
    id: int
    user_id: int
    hotel_id: int
    rating: int
    comment: str
    created_date: date


class BookingInputSchema(BaseModel):
    user_id: int
    hotel_id: int
    room_id: int
    room_image: str
    check_in: datetime
    check_out: datetime
    created_date: date


class BookingOutSchema(BaseModel):
    id: int
    user_id: int
    hotel_id: int
    room_id: int
    room_image: str
    check_in: datetime
    check_out: datetime
    created_date: date











