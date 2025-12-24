# app/services/booking_state.py
from sqlalchemy.orm import Session
from app.crud import BookingRepository

class BookingState:
    name = "base"

    def __init__(self, db: Session):
        self.db = db
        self.booking_repo = BookingRepository(db)

    def transition(self, booking, new_state_class):
        # Используем Repository для обновления
        booking = self.booking_repo.update(booking, status=new_state_class.name)
        return booking


class ReservedState(BookingState):
    name = "reserved"

    def activate(self, booking):
        return self.transition(booking, ActiveState)

    def cancel(self, booking):
        return self.transition(booking, CanceledState)


class ActiveState(BookingState):
    name = "active"

    def complete(self, booking):
        return self.transition(booking, CompletedState)

    def cancel(self, booking):
        return self.transition(booking, CanceledState)


class CompletedState(BookingState):
    name = "completed"


class CanceledState(BookingState):
    name = "canceled"