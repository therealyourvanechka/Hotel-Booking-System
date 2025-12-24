#!/bin/bash
# run_services.sh

# Kill existing processes on these ports if any (just in case)
lsof -ti:8001 | xargs kill -9 2>/dev/null
lsof -ti:8002 | xargs kill -9 2>/dev/null
lsof -ti:8003 | xargs kill -9 2>/dev/null

# Start Guest Service
echo "Starting Guest Service on :8001..."
cd services/guest_service && python3 -m uvicorn src.main:app --port 8001 --reload &
PID_GUEST=$!

# Start Room Service
echo "Starting Room Service on :8002..."
cd services/room_service && python3 -m uvicorn src.main:app --port 8002 --reload &
PID_ROOM=$!

# Start Booking Service
echo "Starting Booking Service on :8003..."
cd services/booking_service && python3 -m uvicorn src.main:app --port 8003 --reload &
PID_BOOKING=$!

echo "Services started. PIDs: $PID_GUEST, $PID_ROOM, $PID_BOOKING"
echo "Press Ctrl+C to stop all services."

trap "kill $PID_GUEST $PID_ROOM $PID_BOOKING" SIGINT
wait
