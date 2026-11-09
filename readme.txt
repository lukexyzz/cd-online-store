
PROJECT OVERVIEW
This project is a web application consisting of:
1. React Single Page Application (Vite) in `frontend/`
2. Python Flask REST API in `backend/`
3. SQLAlchemy (PostgreSQL / SQLite fallback) & PyMongo (MongoDB) in `backend/database/`


PREREQUISITES

- Python 3.9+ installed and added to PATH
- Node.js 18+ and npm installed
- (Optional) PostgreSQL and MongoDB instances if not using the built-in local fallbacks


1. HOW TO RUN THE BACKEND (FLASK API)
Open a PowerShell terminal in the project root (`online-cd-store`) and run:

    cd backend
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt

(Optional) Create your environment file from the template:

    Copy-Item .env.example .env

Start the Flask server:

    python app.py

The API will start at: http://localhost:5000



2. HOW TO RUN BACKEND TESTS (PYTEST)
With the backend virtual environment activated (`backend/.venv`), run:

    cd backend
    .\.venv\Scripts\pytest


3. HOW TO RUN THE FRONTEND (REACT + VITE)
Open a second PowerShell terminal in the project root (`online-cd-store`) and run:

    cd frontend
    npm install
    npm run dev

Then open the URL shown in your terminal (default: http://localhost:5173) in your browser.

