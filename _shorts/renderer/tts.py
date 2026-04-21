"""F5-TTS wrapper.

Uses the Python API so the model loads once per build (not once per beat).
Falls back to the bundled English reference. When Elvis records a voice
sample, swap REF_AUDIO + REF_TEXT to his clip.
"""
from pathlib import Path
import subprocess
import sys

_F5TTS_INSTANCE = None

DEFAULT_REF_AUDIO = Path(
    r"C:\Users\elvis\AppData\Local\Programs\Python\Python312\Lib\site-packages"
    r"\f5_tts\infer\examples\basic\basic_ref_en.wav"
)
DEFAULT_REF_TEXT = "Some call me nature, others call me mother nature."


def _get_model():
    global _F5TTS_INSTANCE
    if _F5TTS_INSTANCE is None:
        from f5_tts.api import F5TTS
        _F5TTS_INSTANCE = F5TTS(model="F5TTS_v1_Base", device="cuda")
    return _F5TTS_INSTANCE


def synthesize(text: str, output_path: Path,
               ref_audio: Path = None, ref_text: str = None,
               speed: float = 1.0) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ref_audio = ref_audio or DEFAULT_REF_AUDIO
    ref_text = ref_text or DEFAULT_REF_TEXT
    model = _get_model()
    wav, sr, _ = model.infer(
        ref_file=str(ref_audio),
        ref_text=ref_text,
        gen_text=text,
        speed=speed,
        remove_silence=True,
        file_wave=str(output_path),
    )
    return output_path


def audio_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout.strip())
