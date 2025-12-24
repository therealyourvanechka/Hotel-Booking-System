from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database
from .hotel_facade import HotelFacade

app = FastAPI(title="Booking Service")

@app.on_event("startup")
def on_startup():
    database.init_db()

@app.post("/bookings/", response_model=schemas.BookingResponse)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(database.get_db)):
    facade = HotelFacade(db)
    try:
        new_booking = facade.book_room(
            passport=booking.guest_passport,
            room_number=booking.room_number,
            check_in=booking.check_in,
            check_out=booking.check_out,
            full_name=booking.guest_name,
            phone=booking.guest_phone
        )
        return new_booking
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

@app.post("/bookings/{booking_id}/activate")
def activate_booking(booking_id: int, db: Session = Depends(database.get_db)):
    facade = HotelFacade(db)
    try:
        return facade.update_booking_status(booking_id, "activate")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/bookings/{booking_id}/pay")
def pay_booking(booking_id: int, db: Session = Depends(database.get_db)):
    # Simply create stub for payment or just complete
    facade = HotelFacade(db)
    try:
         # Assuming pay means complete for now or we add a state
         # original code had complete
        return facade.update_booking_status(booking_id, "complete")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/bookings/{booking_id}/cancel")
def cancel_booking(booking_id: int, db: Session = Depends(database.get_db)):
    facade = HotelFacade(db)
    try:
        return facade.update_booking_status(booking_id, "cancel")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
