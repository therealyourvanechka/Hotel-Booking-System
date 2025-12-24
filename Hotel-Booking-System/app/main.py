from fastapi import FastAPI
from app.db import init_db
from app.routes import hotel

app = FastAPI(title="Hotel Booking System")

init_db()  #  создаёт таблицы при запуске Python-файла

app.include_router(hotel.router)
