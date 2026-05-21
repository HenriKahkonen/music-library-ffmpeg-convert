from utils.constants import ffmpeg_audiocontainers
import os
from pathlib import Path
import shutil

def isAudioFile(file) -> bool:
    """Returns True or False depending on whether or not the file's extension is found in the ffmpeg audio container file extensions."""
    file_extension = os.path.splitext(file)[1]
    if file_extension in ffmpeg_audiocontainers:
        return True
    return False

def getExtension(filename) -> str:
    """Returns the file extension of file"""
    return Path(filename).suffix

def calculateNewAverage(oldaverage, instances, newvalue):
    oldvaluestotal = oldaverage*instances
    newvaluestotal = oldvaluestotal + newvalue
    return newvaluestotal / (instances+1)

def copyFileToTarget(sourcepath, targetpath):
    """_summary_

    Args:
        sourcepath (str): Full path of source file
        targetpath (str): Full path of target file

    Raises:
        IOError: If target path isn't writable
    """
    if os.path.isfile(sourcepath):
        try:
            shutil.copy2(sourcepath,targetpath)
        except IOError as e:
            print(f"Error: {e}")
            raise IOError