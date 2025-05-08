#!/bin/bash

# Start the backend server
echo "Starting the backend server..."
cd backend
pip install -r requirements.txt
python3 -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# Wait for the backend to start
sleep 3

# Start the frontend server
echo "Starting the frontend server..."
cd ../canvas-dashboard
npm install --force
npm run dev &
FRONTEND_PID=$!

# Function to handle script termination
cleanup() {
  echo "Shutting down servers..."
  kill $BACKEND_PID
  kill $FRONTEND_PID
  exit 0
}

# Register the cleanup function for when the script is terminated
trap cleanup SIGINT SIGTERM

echo "Both servers are running!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "Press Ctrl+C to stop both servers."

# Keep the script running
wait
