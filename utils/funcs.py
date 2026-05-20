from utils.constants import ffmpeg_audiocontainers
import os

def isAudioFile(file) -> bool:
    """Returns True or False depending on whether or not the file's extension is found in the ffmpeg audio container file extensions."""
    file_extension = os.path.splitext(file)[1]
    if file_extension in ffmpeg_audiocontainers:
        return True
    return False