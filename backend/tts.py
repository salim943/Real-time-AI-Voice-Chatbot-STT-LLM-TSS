from TTS.api import TTS
import tempfile
import os

tts = TTS(
    model_name="tts_models/multilingual/multi-dataset/xtts_v2"
)

async def generate_tts(text: str) -> bytes:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        path = f.name

    try:
        tts.tts_to_file(
            text=text,
            speaker_wav=None,
            language="en",
            file_path=path
        )

        with open(path, "rb") as f:
            return f.read()
    finally:
        if os.path.exists(path):
            os.remove(path)
