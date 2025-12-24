from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database

app = FastAPI(title="Guest Service")

@app.on_event("startup")
def on_startup():
    database.init_db()

@app.post("/guests/", response_model=schemas.GuestResponse)
def create_guest(guest: schemas.GuestCreate, db: Session = Depends(database.get_db)):
    db_guest = db.query(models.Guest).filter(models.Guest.passport == guest.passport).first()
    if db_guest:
        raise HTTPException(status_code=400, detail="Guest already registered")
    
    new_guest = models.Guest(
        passport=guest.passport,
        full_name=guest.full_name,
        phone=guest.phone
    )
    db.add(new_guest)
    db.commit()
    db.refresh(new_guest)
    return new_guest

@app.get("/guests/{passport}", response_model=schemas.GuestResponse)
def read_guest(passport: str, db: Session = Depends(database.get_db)):
    db_guest = db.query(models.Guest).filter(models.Guest.passport == passport).first()
    if db_guest is None:
        raise HTTPException(status_code=404, detail="Guest not found")
    return db_guest
