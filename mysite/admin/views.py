from mysite.database.models import (UserProfile, City, Review,
                                    Room, Service, Hotel)
from sqladmin import ModelView


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.first_name, UserProfile.last_name]


class CityAdmin(ModelView, model=City):
    column_list = [City.id, City.city_name]


class RoomAdmin(ModelView, model=Room):
    column_list = [Room.room_number]


class ServiceAdmin(ModelView, model=Service):
    column_list = [Service.service_name]


class HotelAdmin(ModelView, model=Hotel):
    column_list = [Hotel.hotel_name]


class ReviewAdmin(ModelView, model=Review):
    column_list = [Review.id]


