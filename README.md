# Smart Task Management System

A Python Flask web application with REST APIs, PostgreSQL, Pandas analytics, and WebSocket real-time notifications.

## Tech Stack
- Python + Flask
- PostgreSQL
- REST API
- Pandas & NumPy
- Flask-SocketIO (WebSockets)
- HTML/CSS/JS

## Setup Instructions

### 1. Install dependencies
pip install -r requirements.txt

### 2. Create PostgreSQL database
CREATE DATABASE smart_task_db;
psql -U postgres -d smart_task_db -f schema.sql

### 3. Update config.py with your DB password

### 4. Run the app
python app.py

Open: http://localhost:5000

## API Endpoints
- POST /api/register
- POST /api/login
- GET /api/logout
- POST /api/tasks
- GET /api/tasks
- PUT /api/tasks/<id>
- DELETE /api/tasks/<id>
- GET /api/analytics

## Features
- User Registration and Login
- Add, View, Update, Delete Tasks
- Analytics with Pandas and NumPy
- Real-time WebSocket notifications
- Clean responsive UI
