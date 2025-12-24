from sqlalchemy.orm import Session
from sqlalchemy import and_
from .models import Booking
from .integration import RoomAdapter

class Handler:
    """Базовый обработчик цепочки."""
    def __init__(self, db: Session):
        self.db = db
        self._next = None

    def set_next(self, handler):
        self._next = handler
        return handler

    def handle(self, data):
        if self._next:
            return self._next.handle(data)
        return data

class DateValidationHandler(Handler):
    """Проверяет валидность дат бронирования."""
    
    def handle(self, data):
        check_in = data["check_in"]  
        check_out = data["check_out"] 
        
        # 1. Базовая валидность дат
        if check_out < check_in:
            raise ValueError(
                f"Дата выезда ({check_out}) должна быть ПОСЛЕ даты заезда ({check_in})")
        
        # 2. Проверка минимальной продолжительности (минимум 1 день)
        from datetime import timedelta
        min_stay = timedelta(days=1)
        if (check_out - check_in) < min_stay:
            raise ValueError(f"Минимальное пребывание - {min_stay.days} день")
        
        # 3. Проверка что даты не в прошлом
        from datetime import date
        if check_in < date.today():
            raise ValueError(f"Дата заезда ({check_in}) не может быть в прошлом")
                
        return super().handle(data)
    
class RoomExistsHandler(Handler):
    def handle(self, data):
        room_number = data["room_number"]
        # Use RoomAdapter instead of direct DB access
        room = RoomAdapter.get_room(room_number)
        if not room:
            raise ValueError(f"Комната с номером {room_number} не найдена в сервисе комнат.")
        return super().handle(data)

class BookingOverlapHandler(Handler):
    """Проверяет пересечение дат бронирования."""
    def handle(self, data):
        room_number = data["room_number"]
        check_in = data["check_in"]
        check_out = data["check_out"]

        overlapping = (
            self.db.query(Booking)
            .filter(
                Booking.room_number == room_number,
                Booking.status.in_(["reserved", "active"]),
                and_(
                    Booking.check_in < check_out,
                    Booking.check_out > check_in,
                ),
            )
            .first()
        )

        if overlapping:
            raise ValueError(
                f"Выбранные даты ({check_in} — {check_out}) пересекаются "
                f"с существующим бронированием (ID={overlapping.id}, "
                f"{overlapping.check_in} — {overlapping.check_out}, статус={overlapping.status})."
            )

        return super().handle(data)
