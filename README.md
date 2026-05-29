# Realtime Voice AI (Local)

A fully local voice AI assistant using:

- Speech-to-Text: faster-whisper
- LLM
- Text-to-Speech: Coqui XTTS v2
- Backend: FastAPI + WebSockets
- Frontend: HTML/CSS/JavaScript

## Setup
```

### 2. Install Python dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Start backend

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

### 4. Start frontend

```bash
cd ../frontend
python -m http.server 5500
```

Open:
http://localhost:5500

## Notes

- First launch may download Whisper and XTTS models.
- CPU works, but GPU is strongly recommended for low latency.
