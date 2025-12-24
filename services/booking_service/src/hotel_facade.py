from sqlalchemy.orm import Session
from datetime import date
from .models import Booking
from .booking_state import ReservedState, ActiveState, CompletedState, CanceledState, BookingState
from .booking_chain import DateValidationHandler, RoomExistsHandler, BookingOverlapHandler
from .integration import GuestAdapter, RoomAdapter

class HotelFacade:
    """Фасад для работы с бронированиями (основной сервис)"""

    def __init__(self, db: Session):
        self.db = db
    
    def _get_or_create_guest(self, passport: str, full_name: str, phone: str = None):
        # Call Guest Service
        guest = GuestAdapter.get_guest(passport)
        if not guest:
            # Create if not exists
            if not full_name or not phone:
                 raise ValueError("Для создания гостя требуются ФИО и телефон")
            guest = GuestAdapter.create_guest(passport, full_name, phone)
        return guest
    
    def book_room(self, passport: str, room_number: int, check_in: date, check_out: date, 
                  full_name: str = None, phone: str = None):
        # 1. Validate logic (Chain)
        date_check = DateValidationHandler(self.db)
        room_check = RoomExistsHandler(self.db)
        overlap_check = BookingOverlapHandler(self.db)
        
        # Chain: dates -> room (remote) -> overlap (local)
        date_check.set_next(room_check).set_next(overlap_check)
        
        request = {
            "room_number": room_number,
            "check_in": check_in,
            "check_out": check_out
        }
        
        date_check.handle(request)
        
        # 2. Handle Guest (remote)
        # We need guest details if we want to create them. Assumes they are passed if potentially new.
        # If the user only passed passport, existing guest check is performed.
        if full_name and phone:
             self._get_or_create_guest(passport, full_name, phone)
        else:
            # Check if guest exists
             guest = GuestAdapter.get_guest(passport)
             if not guest:
                 raise ValueError(f"Гость с паспортом {passport} не найден. Требуются данные для регистрации.")

        # 3. Create Booking (local)
        booking = Booking(
            passport=passport,
            room_number=room_number,
            check_in=check_in,
            check_out=check_out,
            status="reserved"
        )
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        
        return booking

    def update_booking_status(self, booking_id: int, action: str):
        booking = self.db.query(Booking).filter(Booking.id == booking_id).first()
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

        if booking.status == "reserved" and action == "activate":
            return state.activate(booking)
        elif booking.status == "active" and action == "complete":
            return state.complete(booking)
        elif action == "cancel" and booking.status in ["reserved", "active"]:
            return state.cancel(booking)
        else:
            raise ValueError(f"Нельзя выполнить действие '{action}' при статусе '{booking.status}'")
