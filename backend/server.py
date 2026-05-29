from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from stt import transcribe_audio
from llm import stream_llm
from tts import generate_tts

app = FastAPI(title="Realtime Voice AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    print("Client connected")

    try:
        while True:
            audio_bytes = await ws.receive_bytes()

            print("Transcribing...")
            text = await transcribe_audio(audio_bytes)

            if not text:
                await ws.send_text("USER: [No speech detected]")
                continue

            print("USER:", text)
            await ws.send_text(f"USER: {text}")

            llm_text = ""

            async for token in stream_llm(text):
                llm_text += token
                await ws.send_text(f"AI_TOKEN:{token}")

            print("Generating TTS...")
            audio = await generate_tts(llm_text)

            await ws.send_text("AI_DONE")
            await ws.send_bytes(audio)

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print("Error:", e)
