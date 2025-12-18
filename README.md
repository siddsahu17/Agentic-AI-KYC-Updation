# Agentic KYC Platform

A fintech-grade Agentic KYC Updation Platform built with FastAPI and React.

## Features
- User Authentication (JWT)
- Document Upload (Aadhaar, PAN)
- AI Agent Stub for Data Extraction
- KYC Review & Confirmation Interface
- Status Tracking

## Tech Stack
- **Backend:** Python, FastAPI, SQLAlchemy, SQLite (Dev), Pydantic
- **Frontend:** React, Vite, Tailwind CSS, Axios

## Setup Instructions

### Backend
1. Navigate to `backend/`
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
   Server will start at `http://localhost:8000`

### Frontend
1. Navigate to `frontend/`
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the dev server:
   ```bash
   npm run dev
   ```
   App will start at `http://localhost:5173`

## Usage Flow
1. Register a new account at `/login`
2. Login to access the Dashboard
3. Click "Start KYC" to upload documents
4. Upload dummy Aadhaar/PAN images
5. Wait for the "AI Agent" (Stub) to process
6. Review the extracted data and confirm
7. View success status

## Future Improvements
- Integrate real OCR (Tesseract/Google Vision)
- Implement real-time notifications
- Add admin portal for manual verification
