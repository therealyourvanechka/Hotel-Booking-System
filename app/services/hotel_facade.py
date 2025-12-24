# app/services/hotel_facade.py
from sqlalchemy.orm import Session
from app.models import Guest, Booking, Room 
from app.services.booking_state import ReservedState, ActiveState, CompletedState, CanceledState
from app.services.booking_chain import DateValidationHandler, RoomExistsHandler, BookingOverlapHandler
from app.crud import GuestRepository, BookingRepository, RoomRepository, ModelFactory
from datetime import date


class HotelFacade:
    """Фасад для работы с гостями, комнатами и бронированиями"""

    def __init__(self, db: Session):
        self.db = db
        self.guest_repo = GuestRepository(db)
        self.booking_repo = BookingRepository(db)
        self.room_repo = RoomRepository(db)
    
    def _get_or_create_guest(self, passport: str, full_name: str, phone: str = None):
        guest_repo = GuestRepository(self.db)
        guest = guest_repo.get(passport=passport)  
        
        if not guest:
            guest = ModelFactory.create_guest(passport, full_name, phone)
            guest = guest_repo.add(guest)
        
        return guest
    
    def book_room_with_registration(self, passport: str, full_name: str, room_number: int, 
                               check_in: date, check_out: date, phone: str):
        """
        Бронирование с автоматической регистрацией гостя
        """
        # Создаем цепочку проверок
        date_check = DateValidationHandler(self.db)
        room_check = RoomExistsHandler(self.db)
        overlap_check = BookingOverlapHandler(self.db)
        
        # Собираем цепочку: даты → комната → пересечения
        date_check.set_next(room_check).set_next(overlap_check)
        
        request = {
            "room_number": room_number,
            "check_in": check_in,
            "check_out": check_out
        }
        
        # Запускаем все проверки через цепочку
        date_check.handle(request)
        
        # Только после успешной проверки - создать гостя и бронь
        guest = self._get_or_create_guest(passport, full_name, phone)
        
        booking = ModelFactory.create_booking(
            passport=passport,
            room_number=room_number,
            check_in=check_in,
            check_out=check_out,
            status="reserved"
        )
        
        booking_repo = BookingRepository(self.db)
        booking = booking_repo.add(booking)
        
        return booking


    def get_guest_bookings(self, passport: str):
        # Используем Repository для получения данных
        guest = self.guest_repo.get(passport=passport)
        if not guest:
            raise ValueError(f"Гость с паспортом {passport} не найден в системе.")

        bookings = self.booking_repo.get_all(passport=passport)
        return bookings
    
    def get_available_rooms(self, check_in: date, check_out: date):
        """
        Найти все свободные комнаты на указанные даты
        Использует цепочку для валидации дат
        """
        
        date_validator = DateValidationHandler(self.db)
        
        # Просто передаем даты через цепочку для валидации
        request = {
            "check_in": check_in,
            "check_out": check_out,
            "room_number": 0  # Фиктивное значение, т.к. для валидации дат не нужен номер
        }
        
        # Если даты невалидны - DateValidationHandler выбросит исключение
        date_validator.handle(request)

        # Исключаем занятые комнаты
        occupied_rooms_subquery = (
            self.db.query(Booking.room_number)
            .filter(
                Booking.status.in_(["reserved", "active"]),
                Booking.check_in < check_out,
                Booking.check_out > check_in,
            )
            .subquery()
        )
        
        # Ищем все свободные комнаты
        available_rooms = (
            self.db.query(Room)
            .filter(~Room.room_number.in_(self.db.query(occupied_rooms_subquery)))
            .order_by(Room.room_number)
            .all()
        )
        
        return available_rooms

    def register_guest(self, passport: str, full_name: str, phone: str):
        # Используем Repository для проверки существования
        existing = self.guest_repo.get(passport=passport)
        if existing:
            raise ValueError(f"Гость с паспортом {passport} уже зарегистрирован")

        # Используем Factory Method для создания гостя
        guest = ModelFactory.create_guest(passport, full_name, phone)
        
        # Используем Repository для сохранения
        guest = self.guest_repo.add(guest)
        return guest

    def update_booking_status(self, booking_id: int, action: str):
        """Меняет статус бронирования с учётом допустимых переходов."""
        # Используем Repository для получения бронирования
        booking = self.booking_repo.get(id=booking_id)
        if not booking:
            raise ValueError(f"Бронирование c id {booking_id} не найдено")

        state_map = {
            "reserved": ReservedState,
            "active": ActiveState,
            "completed": CompletedState,
            "canceled": CanceledState,
        }
        current_state_class = state_map.get(booking.status, ReservedState)
        state = current_state_class(self.db)

        # Допустимые действия
        if booking.status == "reserved" and action == "activate":
            return state.activate(booking)
        elif booking.status == "active" and action == "complete":
            return state.complete(booking)
        elif action == "cancel" and booking.status in ["reserved", "active"]:
            return state.cancel(booking)
        else:
            raise ValueError(f"Нельзя выполнить действие '{action}' при статусе '{booking.status}'")