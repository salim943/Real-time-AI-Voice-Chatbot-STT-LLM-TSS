'''
from faster_whisper import WhisperModel
import tempfile
import os

# Auto-detect device for broader compatibility
try:
    import torch
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    COMPUTE_TYPE = "float16" if DEVICE == "cuda" else "int8"
except Exception:
    DEVICE = "cpu"
    COMPUTE_TYPE = "int8"

model = WhisperModel(
    "base",
    device=DEVICE,
    compute_type=COMPUTE_TYPE
)

async def transcribe_audio(audio_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_bytes)
        temp_path = f.name

    try:
        segments, _ = model.transcribe(
            temp_path,
            beam_size=1,
            vad_filter=True
        )
        text = "".join(seg.text for seg in segments)
        return text.strip()
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
'''
from faster_whisper import WhisperModel
import tempfile
import subprocess
import os

# Auto-detect device
try:
    import torch
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    COMPUTE_TYPE = "float16" if DEVICE == "cuda" else "int8"
except Exception:
    DEVICE = "cpu"
    COMPUTE_TYPE = "int8"

model = WhisperModel(
    "base",
    device=DEVICE,
    compute_type=COMPUTE_TYPE
)

async def transcribe_audio(audio_bytes: bytes) -> str:

    # Save incoming opus/webm audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as f:
        f.write(audio_bytes)
        input_path = f.name

    wav_path = input_path.replace(".webm", ".wav")

    try:
        # Convert to WAV using ffmpeg
        subprocess.run([
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-ar", "16000",
            "-ac", "1",
            wav_path
        ], check=True)

        segments, _ = model.transcribe(
            wav_path,
            beam_size=1,
            vad_filter=True
        )

        text = "".join(seg.text for seg in segments)

        return text.strip()

    finally:
        for p in [input_path, wav_path]:
            if os.path.exists(p):
                os.remove(p)