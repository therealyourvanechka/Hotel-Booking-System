import requests
import time
import sys

GUEST_URL = "http://localhost:8001"
ROOM_URL = "http://localhost:8002"
BOOKING_URL = "http://localhost:8003"

def wait_for_services():
    print("Waiting for services to be ready...")
    for url in [GUEST_URL, ROOM_URL, BOOKING_URL]:
        for _ in range(10):
            try:
                requests.get(f"{url}/docs")
                break
            except requests.ConnectionError:
                time.sleep(1)
        else:
            print(f"Service {url} not ready.")
            sys.exit(1)
    print("All services ready!")

def run_test():
    # 1. Create a Room
    print("Creating Room 101...")
    room_data = {"room_number": 101, "room_type": "standard", "price": 100.0}
    # Note: Schema requires room_number in body. Check schemas.
    # RoomCreate has room_number so response should be ok.
    # Actually RoomCreate has room_number type int.
    try:
        resp = requests.post(f"{ROOM_URL}/rooms/", json=room_data)
        if resp.status_code == 200:
             print("Room created:", resp.json())
        elif resp.status_code == 400: # Already exists
             print("Room already exists (ok)")
        else:
             print("Error creating room:", resp.text)
             sys.exit(1)
    except Exception as e:
         print(f"Request failed: {e}")
         sys.exit(1)

    # 2. Create Booking (and Guest via facade)
    print("Creating Booking...")
    from datetime import date, timedelta
    today = date.today()
    check_in = (today + timedelta(days=1)).isoformat()
    check_out = (today + timedelta(days=5)).isoformat()
    
    booking_data = {
        "check_in": check_in,
        "check_out": check_out,
        "guest_passport": "AB123456",
        "room_number": 101,
        "guest_name": "John Doe",
        "guest_phone": "+1234567890"
    }
    resp = requests.post(f"{BOOKING_URL}/bookings/", json=booking_data)
    if resp.status_code == 200:
        print("Booking created:", resp.json())
        booking_id = resp.json()["id"]
    else:
        print("Error creating booking:", resp.text)
        sys.exit(1)

    # 3. Check Guest was created
    print("Verifying Guest creation...")
    resp = requests.get(f"{GUEST_URL}/guests/AB123456")
    if resp.status_code == 200:
        print("Guest found:", resp.json())
    else:
        print("Guest not found!")
        sys.exit(1)
        
    # 4. Activate Booking
    print("Activating Booking...")
    resp = requests.post(f"{BOOKING_URL}/bookings/{booking_id}/activate")
    if resp.status_code == 200:
        print("Booking activated:", resp.json())
    else:
        print("Error activating booking:", resp.text)
        sys.exit(1)
        
    print("\nSUCCESS: E2E Test Passed!")

if __name__ == "__main__":
    wait_for_services()
    run_test()
