"""Storyboard schema + YAML loader.

A storyboard is an ordered list of beats. Each beat is one action in the
warehouse analogy: the user asks for something, the robot fetches it, or the
robot self-acts on a lane. Durations are determined at render time by the
length of the synthesized narration audio.
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import yaml

BEAT_KINDS = {"open", "call", "return", "self", "finale"}


@dataclass
class Beat:
    kind: str
    from_lane: Optional[str] = None
    to_lane: Optional[str] = None
    label: str = ""
    narration: str = ""
    min_duration: float = 1.4
    hold_after: float = 0.25
    audio_path: Optional[Path] = None
    audio_duration: float = 0.0
    start_time: float = 0.0
    duration: float = 0.0
    event_world_x: float = 0.0

    def __post_init__(self):
        if self.kind not in BEAT_KINDS:
            raise ValueError(f"Unknown beat kind: {self.kind}")


@dataclass
class Storyboard:
    lesson_id: str
    day_number: int
    learning_title: str
    lesson_title: str
    lanes: list[str]
    beats: list[Beat]
    hook_text: str = ""
    finale_hold: float = 3.0

    @classmethod
    def from_yaml(cls, path: Path) -> "Storyboard":
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        beats_raw = data.pop("beats")
        beats = [Beat(**b) for b in beats_raw]
        return cls(beats=beats, **data)

    @property
    def total_duration(self) -> float:
        if not self.beats:
            return 0.0
        last = self.beats[-1]
        return last.start_time + last.duration + self.finale_hold
