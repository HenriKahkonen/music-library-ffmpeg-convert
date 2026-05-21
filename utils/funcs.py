from utils.constants import ffmpeg_audiocontainers
import os
from pathlib import Path
import shutil
from ffmpeg import FFmpeg

def isAudioFile(file:str) -> bool:
    """Returns True or False depending on whether or not the file's extension is found in the ffmpeg audio container file extensions."""
    file_extension = os.path.splitext(file)[1]
    if file_extension in ffmpeg_audiocontainers:
        return True
    return False

def getExtension(filename:str) -> str:
    """Returns the file extension of file"""
    return Path(filename).suffix

def calculateNewAverage(oldaverage, instances, newvalue):
    oldvaluestotal = oldaverage*instances
    newvaluestotal = oldvaluestotal + newvalue
    return newvaluestotal / (instances+1)

def copyFileToTarget(sourcepath:str, targetpath:str):
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
        
def transcodeAudioToTarget(inputpath:str,outputpath:str,targetcontainer:str):
    """_summary_

    Args:
        inputpath (str): full path of input file
        outputpath (str): full path of output file
        targetcontainer (str): for example '.mp3'

    Raises:
        TypeError: If transcoding to a container not currently supported

    Returns:
        bool: True or False depending on whether file was transcoded
    """

    supportedContainers = [".mp3"]
    if targetcontainer not in supportedContainers:
        raise TypeError(f"Target container {targetcontainer} is not currently supported by script.")
    
    sourcecontainer = Path(inputpath).suffix
    output = outputpath.replace(sourcecontainer,targetcontainer)

    # Skip transcoding if output file already exists
    if os.path.isfile(output):
        return False
    
    # Convert to .mp3
    if targetcontainer == ".mp3":

        ffmpeg = (
            FFmpeg()
            .option("y")
            .input(inputpath)
            .output(
                output,
                {"codec:a": "libmp3lame"},
            )
        )

        ffmpeg.execute()

        return True