from fastapi import FastAPI
from mysite.api import users, hotel, review, city, room_image, room, hotel_image, booking, service, auth
import uvicorn
from mysite.admin.setup import setup_admin

booking_app = FastAPI(title='Tyky Project')
booking_app.include_router(users.user_router)
booking_app.include_router(hotel.hotel_router)
booking_app.include_router(review.review_router)
booking_app.include_router(city.city_router)
booking_app.include_router(room_image.room_image_router)
booking_app.include_router(room.room_router)
booking_app.include_router(hotel_image.hotel_image_router)
booking_app.include_router(booking.booking_router)
booking_app.include_router(service.service_router)
booking_app.include_router(auth.auth_router)
setup_admin(booking_app)

if __name__ == '__main__':
    uvicorn.run(booking_app, host='127.0.0.1', port=8005)


