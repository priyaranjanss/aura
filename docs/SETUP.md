# AURA – Setup & Installation Guide

This guide will help you set up the complete AURA Voice Assistant from scratch on your laptop.

---

## 1. Prerequisites

Make sure you have the following installed:

### Required Software
- **Python 3.10+** → [Download](https://www.python.org/downloads/)
- **Node.js 18+** → [Download](https://nodejs.org/)
- **Git** (optional but recommended)
- **Google Chrome** (best browser for microphone access)

### Check Versions
Open terminal/command prompt and run:

```bash
python --version
node --version
npm --version
```

---

## 2. Get Google Gemini API Key

1. Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **Create API Key**
4. Copy the key (you will need it later)

---

## 3. Project Setup

### Step 1: Create Project Folder

```bash
mkdir aura-assistant
cd aura-assistant
```

### Step 2: Backend Setup

```bash
mkdir backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Create requirements.txt and install
pip install fastapi uvicorn python-dotenv google-generativeai edge-tts pyautogui pillow pydantic
```

Create a file named `.env` inside `backend/` folder:

```
GEMINI_API_KEY=your_actual_api_key_here
HOST=127.0.0.1
PORT=8000
```

### Step 3: Frontend Setup

Open a **new terminal** and go back to the project root:

```bash
cd aura-assistant
npm create vite@latest frontend -- --template react
cd frontend
npm install
npm install axios tailwindcss postcss autoprefixer zustand
npx tailwindcss init -p
```

---

## 4. Running the Application

### Start Backend

```bash
cd backend
# Activate venv if not already active
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend will run at: **http://127.0.0.1:8000**

### Start Frontend

Open another terminal:

```bash
cd frontend
npm run dev
```

Frontend will run at: **http://localhost:5173**

---

## 5. First Run Checklist

- [ ] Backend is running without errors
- [ ] Frontend opens in browser
- [ ] Microphone permission is allowed
- [ ] Gemini API key is correctly set in `.env`
- [ ] You can type a message and get a reply

---

## 6. Common Issues & Solutions

| Problem                        | Solution                                      |
|--------------------------------|-----------------------------------------------|
| Microphone not working         | Use Chrome + allow permission                 |
| Gemini API error               | Check API key in `.env`                       |
| CORS error                     | Make sure backend CORS is enabled             |
| Module not found               | Activate virtual environment                  |
| Port already in use            | Change port or kill previous process          |
| pyautogui not working on Mac   | Give Accessibility permission to Terminal     |

---

## 7. Folder Structure After Setup

```
aura-assistant/
├── backend/
│   ├── app/
│   ├── venv/
│   ├── .env
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
├── README.md
├── SETUP.md
└── ...
```

---

## 8. Recommended Development Order

1. Setup backend + basic FastAPI hello world
2. Setup React frontend + basic UI
3. Connect frontend to backend
4. Add system commands
5. Add Gemini AI
6. Add speech features
7. Polish UI

---

**You are now ready to start development.**
