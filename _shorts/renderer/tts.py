"""Text-to-speech backends.

Two engines are supported. The default is **Kokoro-82M** (warm built-in voices,
no reference clip needed, fast GPU inference). F5-TTS v1 Base stays in the
codebase as the voice-cloning path for when Elvis records his own voice
sample — swap `VOICE_ENGINE` to `"f5_tts"` and update DEFAULT_REF_AUDIO.

The model is loaded once per build and reused across beats.
"""
from pathlib import Path
import subprocess

VOICE_ENGINE = "kokoro"  # "kokoro" | "f5_tts"

# Kokoro defaults (warm educator tone)
KOKORO_VOICE = "af_heart"   # warm American female; alt: af_bella, am_adam
KOKORO_SPEED = 0.95         # slightly slower = more "settled" delivery

# F5-TTS defaults (only used when VOICE_ENGINE == "f5_tts")
F5_REF_AUDIO = Path(
    r"C:\Users\elvis\AppData\Local\Programs\Python\Python312\Lib\site-packages"
    r"\f5_tts\infer\examples\basic\basic_ref_en.wav"
)
F5_REF_TEXT = "Some call me nature, others call me mother nature."

_KOKORO_PIPELINE = None
_F5TTS_INSTANCE = None


def _get_kokoro():
    global _KOKORO_PIPELINE
    if _KOKORO_PIPELINE is None:
        from kokoro import KPipeline
        _KOKORO_PIPELINE = KPipeline(
            lang_code="a",                      # American English
            repo_id="hexgrad/Kokoro-82M",
            device="cuda",
        )
    return _KOKORO_PIPELINE


def _get_f5tts():
    global _F5TTS_INSTANCE
    if _F5TTS_INSTANCE is None:
        from f5_tts.api import F5TTS
        _F5TTS_INSTANCE = F5TTS(model="F5TTS_v1_Base", device="cuda")
    return _F5TTS_INSTANCE


def _synth_kokoro(text: str, output_path: Path,
                  voice: str = None, speed: float = None) -> Path:
    import numpy as np
    import soundfile as sf

    pipeline = _get_kokoro()
    voice = voice or KOKORO_VOICE
    speed = speed if speed is not None else KOKORO_SPEED

    chunks = []
    for _graphemes, _phonemes, audio in pipeline(text, voice=voice, speed=speed):
        # Kokoro yields torch.Tensor audio; convert to numpy on CPU for concat/write
        if hasattr(audio, "detach"):
            audio = audio.detach().cpu().numpy()
        chunks.append(np.asarray(audio, dtype=np.float32))
    full = np.concatenate(chunks) if len(chunks) > 1 else chunks[0]
    # Small silence pad at end so beats don't feel clipped
    pad = np.zeros(int(0.15 * 24000), dtype=np.float32)
    full = np.concatenate([full, pad])
    sf.write(str(output_path), full, 24000)
    return output_path


def _synth_f5tts(text: str, output_path: Path,
                 ref_audio: Path = None, ref_text: str = None,
                 speed: float = 1.0) -> Path:
    model = _get_f5tts()
    model.infer(
        ref_file=str(ref_audio or F5_REF_AUDIO),
        ref_text=ref_text or F5_REF_TEXT,
        gen_text=text,
        speed=speed,
        remove_silence=True,
        file_wave=str(output_path),
    )
    return output_path


def synthesize(text: str, output_path: Path, **kwargs) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if VOICE_ENGINE == "kokoro":
        return _synth_kokoro(text, output_path, **kwargs)
    if VOICE_ENGINE == "f5_tts":
        return _synth_f5tts(text, output_path, **kwargs)
    raise ValueError(f"Unknown VOICE_ENGINE: {VOICE_ENGINE}")


def audio_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout.strip())
