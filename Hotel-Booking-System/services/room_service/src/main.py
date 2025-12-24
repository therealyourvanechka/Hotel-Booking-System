from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database

app = FastAPI(title="Room Service")

@app.on_event("startup")
def on_startup():
    database.init_db()

@app.post("/rooms/", response_model=schemas.RoomResponse)
def create_room(room: schemas.RoomCreate, db: Session = Depends(database.get_db)):
    db_room = db.query(models.Room).filter(models.Room.room_number == room.room_number).first()
    if db_room:
        raise HTTPException(status_code=400, detail="Room already exists")
    
    new_room = models.Room(
        room_number=room.room_number,
        room_type=room.room_type,
        price=room.price
    )
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

@app.get("/rooms/{room_number}", response_model=schemas.RoomResponse)
def read_room(room_number: int, db: Session = Depends(database.get_db)):
    db_room = db.query(models.Room).filter(models.Room.room_number == room_number).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room

@app.get("/rooms/", response_model=List[schemas.RoomResponse])
def read_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    rooms = db.query(models.Room).offset(skip).limit(limit).all()
    return rooms
