class ExternalGuestAPI:
    """Имитация внешнего API для получения данных о госте"""
    def get_guest_data(self, passport: str):
        # В реальности здесь был бы запрос к API, например requests.get(...)
        return {
            "passport": passport,
            "full_name": "John Doe",
            "phone": "+123456789"
        }


class GuestAdapter:
    """Адаптер, приводящий внешние данные к формату модели Guest"""
    def __init__(self, external_api: ExternalGuestAPI):
        self.external_api = external_api

    def get_guest_as_dict(self, passport: str):
        data = self.external_api.get_guest_data(passport)
        return {
            "passport": data["passport"],
            "full_name": data["full_name"],
            "phone": data.get("phone"),
        }
