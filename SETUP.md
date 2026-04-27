# 🛠️ Setup & Installation Guide

This guide provides the necessary steps to set up the **Spanish Travel Companion** locally and instructions for testing the integration with external APIs.

## 📋 Prerequisites

Before beginning, ensure you have the following installed:
* **Node.js** (v18 or higher recommended)
* **Python 3.12** (Required for `pydantic_core` compatibility)
* **Git**

---

## 🚀 Local Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/Mathperson271828/Spanish-Travel-Companion.git](https://github.com/Mathperson271828/Spanish-Travel-Companion.git)
cd Spanish-Travel-Companion
```

### 2. Backend Setup (FastAPI)
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows:
   .\\.venv\\Scripts\\activate
   # On Mac/Linux:
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Frontend Setup (Next.js)
1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install the necessary packages:
   ```bash
   npm install
   ```

---

## 🔑 Environment Variables & API Configuration

This project relies on **OpenAI** for its core machine learning pipeline.

### 1. Obtain API Keys
* **OpenAI API Key:** Required for **Whisper-1** (Speech-to-Text), **GPT-4o-mini** (LLM), and **TTS-1** (Speech Synthesis).

### 2. Configure `.env` Files
Create a `.env` file in the **backend** directory:
```env
OPENAI_API_KEY=your_openai_key_here
```

---

## 🏃 Running the Application

### Start the Backend
From the `backend` directory:
```bash
uvicorn main_backend:app --reload --host 0.0.0.0 --port 10000
```

### Start the Frontend
From the `frontend` directory:
```bash
npm run dev
```
Open **http://localhost:3000** in your browser to interact with the application.

## ⚠️ Known Limitations
* **Render Cold Start:** If testing the live production deployment hosted on Render's free tier, the initial request may take up to 50 seconds to process as the server wakes from sleep. Subsequent requests will process within 3-5 seconds.
* **Microphone Permissions:** The browser must be granted microphone access for the Web Audio API and MediaRecorder to function.