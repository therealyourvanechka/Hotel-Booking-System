#!/bin/bash

# 1. Create a Room
echo "Creating Room 101..."
curl -X 'POST' \
  'http://localhost:8002/rooms/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "room_number": 101,
  "room_type": "standard",
  "price": 100.0
}'
echo -e "\n"

# 2. Create a Guest
echo "Creating Guest..."
curl -X 'POST' \
  'http://localhost:8001/guests/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "passport": "12345",
  "full_name": "Ivan Ivanov",
  "phone": "+1234567890"
}'
echo -e "\n"

# 3. Create a Booking
echo "Creating Booking..."
curl -X 'POST' \
  'http://localhost:8003/bookings/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "guest_passport": "12345",
  "room_number": 101,
  "check_in": "2027-01-01",
  "check_out": "2027-01-05",
  "guest_name": "Ivan Ivanov",
  "guest_phone": "+1234567890"
}'
echo -e "\n"
