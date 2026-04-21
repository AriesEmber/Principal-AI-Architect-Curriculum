"""Shorts renderer package.

Pipeline: storyboard YAML -> TTS per beat -> PIL frames -> ffmpeg MP4.
Canvas is 1080x1920 (9:16 vertical), 30 fps. Robot sprite is always centered;
lane content scrolls right-to-left as time advances.
"""
