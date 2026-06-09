from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship, MappedColumn
from sqlalchemy import Integer, String, Enum, Date, ForeignKey, Text, Boolean, DateTime
from typing import Optional, List
from enum import Enum as PyEnum
from datetime import date, datetime


class RoleChoices(str, PyEnum):
    client = 'client'
    owner = 'owner'


class UserProfile(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    user_img: Mapped[str] = mapped_column(String, nullable=True)
    country: Mapped[Optional[int]] = mapped_column(ForeignKey('city.id'), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String,nullable=True)
    user_role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), default=RoleChoices.client)
    register_date: Mapped[date] = mapped_column(Date, default=date.today)


    user_reviews: Mapped[List['Review']] = relationship('Review', back_populates='user',
                                                        cascade='all, delete-orphan')
    bookings: Mapped[List['Booking']] = relationship('Booking', back_populates='user',
                                                     cascade='all, delete-orphan')
    user_tokens: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='token_user',
                                                             cascade='all, delete-orphan')

    def set_password(self, password:str):
        self.password = bcrypt.hash(password)

    def __repr__(self):
        return f'{self.first_name}, {self.last_name}'



class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    token_user: Mapped[UserProfile] = relationship('UserProfile',
                                                   back_populates='user_tokens')



class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_image: Mapped[str] = mapped_column(String)
    city_name: Mapped[str] = mapped_column(String(80), unique=True)

    hotels: Mapped[List['Hotel']] = relationship('Hotel', back_populates='city')



class Service(Base):
    __tablename__ = 'service'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    service_image: Mapped[str] = mapped_column(String)
    service_name: Mapped[str] = mapped_column(String(30), unique=True)

    hotels: Mapped[List['Hotel']] = relationship('Hotel', back_populates='service',
                                                 cascade='all, delete-orphan')



class Hotel(Base):
    __tablename__ = 'hotel'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_name: Mapped[str] = mapped_column(String(50))
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    country: Mapped[int] = mapped_column(Integer)
    street: Mapped[str] = mapped_column(String(40), unique=True)
    postal_code: Mapped[int] = mapped_column(Integer, nullable=True)
    hotel_stars: Mapped[int] = mapped_column(Integer, nullable=True)
    description: Mapped[str] = mapped_column(Text)
    service_id: Mapped[int] = mapped_column(ForeignKey('service.id'))


    service: Mapped['Service'] = relationship('Service', back_populates='hotels')
    rooms: Mapped[List['Room']] = relationship('Room', back_populates='hotel',
                                               cascade='all, delete-orphan')
    hotels_image: Mapped[List['HotelImage']] = relationship('HotelImage', back_populates='hotel',
                                                            cascade='all, delete-orphan')
    reviews: Mapped[List['Review']] = relationship('Review', back_populates='hotel',
                                                   cascade='all, delete-orphan')
    bookings: Mapped[List['Booking']] = relationship('Booking', back_populates='hotel',
                                                     cascade='all, delete-orphan')
    city: Mapped['City'] = relationship('City', back_populates='hotels')




class HotelImage(Base):
    __tablename__ = 'hotel_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_id: Mapped[int]  = mapped_column(ForeignKey('hotel.id'))
    hotel_image: Mapped[str] = mapped_column(String)

    hotel: Mapped['Hotel'] = relationship(Hotel, back_populates='hotels_image')



class RoomTypeChoices(str, PyEnum):
    luxury = 'luxury'
    family = 'family'
    economy = 'economy'
    single = 'single'



class Room(Base):
    __tablename__ = 'room'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    room_number: Mapped[int] = mapped_column(Integer, nullable=True)
    price: Mapped[int] = mapped_column(Integer)
    room_type: Mapped[RoomTypeChoices] = mapped_column(Enum(RoomTypeChoices), default=RoomTypeChoices.single)
    description: Mapped[str] = mapped_column(Text)


    bookings: Mapped[List['Booking']] = relationship('Booking', back_populates='room',
                                                     cascade='all, delete-orphan')
    rooms: Mapped[List['RoomImage']] = relationship('RoomImage', back_populates='room',
                                                    cascade='all, delete-orphan')
    hotel: Mapped['Hotel'] = relationship('Hotel', back_populates='rooms')




class RoomImage(Base):
    __tablename__ = 'room_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    room_image: Mapped[str] = mapped_column(String)

    room: Mapped[int] = relationship(Room, back_populates='rooms')




class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] =mapped_column(ForeignKey('users.id'))
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(Text)
    created_date: Mapped[date] = mapped_column(Date, default=date.today)

    hotel: Mapped['Hotel'] = relationship('Hotel', back_populates='reviews')
    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='user_reviews')



class Booking(Base):
    __tablename__ = 'booking'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    room_image: Mapped[str] = mapped_column(String)
    check_in: Mapped[datetime] = mapped_column(DateTime)
    check_out: Mapped[datetime] = mapped_column(DateTime)
    created_date: Mapped[date] = mapped_column(Date, default=date.today)


    room: Mapped['Room'] = relationship('Room', back_populates='bookings')
    hotel: Mapped['Hotel'] = relationship('Hotel', back_populates='bookings')
    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='bookings')
















