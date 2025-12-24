# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional

# ============================================================
# Factory Method
# ============================================================

class ModelFactory:
    """
    Класс-фабрика для создания ORM-моделей.
    """

    @staticmethod
    def create_guest(passport: str, full_name: str, phone: Optional[str] = None) -> models.Guest:
        """Создаёт объект модели Guest."""
        return models.Guest(
            passport=passport,
            full_name=full_name,
            phone=phone
        )

    @staticmethod
    def create_booking(passport: str, room_number: int, check_in, check_out, status: str = "reserved") -> models.Booking:
        """Создаёт объект модели Booking."""
        return models.Booking(
            passport=passport,
            room_number=room_number,
            check_in=check_in,
            check_out=check_out,
            status=status
        )


# ============================================================
#  Repository
# ============================================================

class BaseRepository:
    """
    Базовый репозиторий, предоставляющий общие CRUD-методы.
    """

    def __init__(self, db: Session, model):
        self.db = db
        self.model = model

    def add(self, instance):
        """Добавление объекта в базу."""
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def get(self, **filters):
        """Получение одного объекта по фильтрам."""
        return self.db.query(self.model).filter_by(**filters).first()

    def get_all(self, **filters):
        """Получение всех объектов модели с возможностью фильтрации."""
        query = self.db.query(self.model)
        if filters:
            query = query.filter_by(**filters)
        return query.all()

    def update(self, instance, **update_data):
        """Обновление объекта."""
        for key, value in update_data.items():
            setattr(instance, key, value)
        self.db.commit()
        self.db.refresh(instance)
        return instance


class GuestRepository(BaseRepository):
    """Репозиторий для модели Guest."""
    def __init__(self, db: Session):
        super().__init__(db, models.Guest)


class BookingRepository(BaseRepository):
    """Репозиторий для модели Booking."""
    def __init__(self, db: Session):
        super().__init__(db, models.Booking)


class RoomRepository(BaseRepository):
    """Репозиторий для модели Room."""
    def __init__(self, db: Session):
        super().__init__(db, models.Room)