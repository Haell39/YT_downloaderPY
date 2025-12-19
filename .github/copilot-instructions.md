# YouTube Downloader & MP3 Converter - AI Coding Guide

## Project Overview

Simple Python YouTube downloader with MP3 conversion capability. Two standalone scripts:

- [app.py](../app.py): Downloads YouTube videos via command-line argument
- [convert.py](../convert.py): Converts video files to MP3 audio

**Language**: Portuguese (Brazilian) - Comments, print statements, and user-facing text should be in PT-BR.

## Core Architecture

### Two Independent Scripts

- **app.py**: Uses `pytubefix` library, takes YouTube URL as `sys.argv[1]`, saves to `videos/` folder
- **convert.py**: Uses `moviepy` library with `argparse`, takes video path as argument, saves to `MP3/` folder
- No shared code/modules between scripts - each is self-contained

### Directory Structure

```
videos/     - Auto-created by app.py for downloaded videos
MP3/        - Auto-created by convert.py for extracted audio
```

## Key Patterns & Conventions

### Command-Line Interface

- **app.py**: Uses `sys.argv[1]` for simple single-argument URL input
  ```bash
  python app.py "https://www.youtube.com/watch?v=..."
  ```
- **convert.py**: Uses `argparse` for video file path with error messages
  ```bash
  python convert.py "videos/video_name.mp4"
  ```

### Folder Auto-Creation Pattern

Both scripts check for and create output directories:

```python
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
```

### Resource Management

convert.py explicitly closes video/audio clips after processing:

```python
audio_clip.close()
video_clip.close()
```

## Dependencies

- `pytubefix`: YouTube download (not `pytube`)
- `moviepy`: Video to MP3 conversion
- Install: `pip install -r requirements.txt`

## Development Workflow

**No tests, build system, or CI/CD** - Simple utility scripts run directly via Python CLI.

**Running the tools:**

1. Download: `python app.py "YOUTUBE_URL"`
2. Convert: `python convert.py "videos/filename.mp4"`

## Code Style Notes

- Portuguese variable names and comments (e.g., `audio_folder`, `video_path`)
- User messages in Portuguese: `"Conversão para MP3 concluída em..."`
- Simple error handling with print statements and early returns
- Informative console output (title, views, progress messages)

## Important Constraints

- app.py downloads **highest resolution only** via `get_highest_resolution()`
- No playlist support - single video URLs only
- No configuration files or settings - hardcoded folder names
- Videos must be in `videos/` folder for convenient conversion workflow
