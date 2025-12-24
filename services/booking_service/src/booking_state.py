from sqlalchemy.orm import Session

class BookingState:
    name = "base"

    def __init__(self, db: Session):
        self.db = db

    def transition(self, booking, new_state_class):
        booking.status = new_state_class.name
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
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
