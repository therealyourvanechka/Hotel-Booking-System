import requests
import os
from fastapi import HTTPException

# URLs for other services (configured via env vars)
GUEST_SERVICE_URL = os.getenv("GUEST_SERVICE_URL", "http://localhost:8001")
ROOM_SERVICE_URL = os.getenv("ROOM_SERVICE_URL", "http://localhost:8002")

class GuestAdapter:
    @staticmethod
    def get_guest(passport: str):
        try:
            response = requests.get(f"{GUEST_SERVICE_URL}/guests/{passport}")
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            # For resilience, we might want to retry or circuit break
            return None

    @staticmethod
    def create_guest(passport: str, full_name: str, phone: str):
        payload = {"passport": passport, "full_name": full_name, "phone": phone}
        response = requests.post(f"{GUEST_SERVICE_URL}/guests/", json=payload)
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=f"Failed to create guest: {response.text}")

class RoomAdapter:
    @staticmethod
    def get_room(room_number: int):
        try:
            response = requests.get(f"{ROOM_SERVICE_URL}/rooms/{room_number}")
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None
