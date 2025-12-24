from datetime import date

"""
Инкапсулирует действие пользователя 
(например: регистрация, бронирование, изменение статуса) 
в отдельный объект-команду
"""

class Command:
    """Базовый интерфейс команды"""
    def execute(self):
        raise NotImplementedError("Метод execute() должен быть реализован")


class RegisterGuestCommand(Command):
    def __init__(self, facade, passport: str, full_name: str, phone: str | None = None):
        self.facade = facade
        self.passport = passport
        self.full_name = full_name
        self.phone = phone

    def execute(self):
        return self.facade.register_guest(self.passport, self.full_name, self.phone)


class BookRoomCommand(Command):
    def __init__(self, facade, passport: str, full_name: str, room_number: int, 
                 check_in: date, check_out: date, phone: str | None = None):
        self.facade = facade
        self.passport = passport
        self.full_name = full_name
        self.room_number = room_number
        self.check_in = check_in
        self.check_out = check_out
        self.phone = phone

    def execute(self):
        return self.facade.book_room_with_registration(
            self.passport, self.full_name, self.room_number,
            self.check_in, self.check_out, self.phone
        )


class UpdateBookingStatusCommand(Command):
    def __init__(self, facade, booking_id: int, action: str):
        self.facade = facade
        self.booking_id = booking_id
        self.action = action

    def execute(self):
        return self.facade.update_booking_status(self.booking_id, self.action)
