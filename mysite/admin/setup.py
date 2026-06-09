from .views import UserProfileAdmin, CityAdmin, RoomAdmin, ServiceAdmin, ReviewAdmin, HotelAdmin
from fastapi import FastAPI
from sqladmin import Admin
from mysite.database.db import engine


def setup_admin(mysite: FastAPI):
    admin = Admin(mysite, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(ServiceAdmin)
    admin.add_view(RoomAdmin)
    admin.add_view(CityAdmin)
    admin.add_view(HotelAdmin)
    admin.add_view(ReviewAdmin)