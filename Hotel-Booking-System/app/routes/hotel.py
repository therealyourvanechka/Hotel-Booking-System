from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.db import get_db
from app.services.hotel_facade import HotelFacade
from app.decorators.logging_decorator import LoggingDecorator
from app.adapters.guest_adapter import GuestAdapter, ExternalGuestAPI
from app.services.command import RegisterGuestCommand, BookRoomCommand, UpdateBookingStatusCommand

router = APIRouter(prefix="/hotel", tags=["Hotel"])

@router.post("/update_booking_status")
def update_booking_status(booking_id: int, action: str, db: Session = Depends(get_db)):
    facade = LoggingDecorator(HotelFacade(db))
    try:
        command = UpdateBookingStatusCommand(facade, booking_id, action)
        booking = command.execute()
        return {"status": "success", "booking_id": booking.id, "new_status": booking.status}
    except ValueError as e:
        return {"status": "error", "message": str(e)}

@router.post("/register_guest")
def register_guest(passport: str, full_name: str, phone: str | None = None, db: Session = Depends(get_db)):
    facade = LoggingDecorator(HotelFacade(db))
    try:
        command = RegisterGuestCommand(facade, passport, full_name, phone)
        guest = command.execute()
        return {"status": "registered", "guest": {"passport": guest.passport, "name": guest.full_name}}
    except ValueError as e:
        return {"status": "error", "message": str(e)}

@router.post("/book_room")
def book_room(passport: str, full_name: str, room_number: int, 
              check_in: str, check_out: str, phone: str, 
              db: Session = Depends(get_db)):
    try:
        facade = LoggingDecorator(HotelFacade(db)) 
        
        from datetime import datetime
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
        
        command = BookRoomCommand(facade, passport, full_name, room_number, 
                                 check_in_date, check_out_date, phone)
        booking = command.execute()
        return {"status": "success", "booking_id": booking.id, "new_status": booking.status}
    except ValueError as e:
        return {"status": "error", "message": str(e)}

@router.get("/available_rooms")
def get_available_rooms(check_in: str, check_out: str, db: Session = Depends(get_db)):
    """Получить список всех свободных номеров на указанные даты"""
    try:
        facade = HotelFacade(db)
        
        # Преобразуем даты
        from datetime import datetime
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
        
        # Получаем свободные комнаты
        rooms = facade.get_available_rooms(check_in_date, check_out_date)
        
        # Рассчитываем общую стоимость
        total_nights = (check_out_date - check_in_date).days
        
        # Формируем ответ
        available_rooms = [
            {
                "room_number": room.room_number,
                "room_type": room.room_type,
                "price_per_night": float(room.price),  # Конвертируем в float для JSON
                "total_price": float(room.price * total_nights)
            }
            for room in rooms
        ]
        
        return {
            "search_period": {
                "check_in": check_in,
                "check_out": check_out,
                "total_nights": total_nights
            },
            "available_rooms": available_rooms
        }
        
    except ValueError as e:
        return {"status": "error", "message": str(e)}
    except Exception as e:
        return {"status": "error", "message": f"Ошибка при поиске: {str(e)}"}
    
@router.get("/guest_bookings/{passport}")
def guest_bookings(passport: str, db: Session = Depends(get_db)):
    facade = HotelFacade(db)
    try:
        bookings = facade.get_guest_bookings(passport)
        return {"bookings": [{"room": b.room_number, "check_in": b.check_in, "check_out": b.check_out, "status": b.status} for b in bookings]}
    except ValueError as e:
        return {"status": "error", "message": str(e)}

@router.post("/import_guest")
def import_guest(passport: str, db: Session = Depends(get_db)):
    """Пример использования Adapter — импорт данных гостя из внешнего API"""
    external_api = ExternalGuestAPI()
    adapter = GuestAdapter(external_api)
    guest_data = adapter.get_guest_as_dict(passport)

    facade = HotelFacade(db)
    guest = facade.register_guest(**guest_data)
    return {"imported_guest": guest_data}
