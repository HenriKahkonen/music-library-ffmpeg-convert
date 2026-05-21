import sys, json, os, math
from datetime import datetime
import utils.exceptions as excepts
from dotenv import dotenv_values
from pathlib import Path

from utils.funcs import isAudioFile, getExtension, calculateNewAverage, copyFileToTarget, transcodeAudioToTarget
from utils.constants import ffmpeg_audiocontainers

def main(argv: list[str]) -> int:

    print("\n"+"="*25+"Music library converter tool"+"="*25+"\n")
    
    #  ================
    #  Pre-operation validations
    #  ================

    timetostartpreparations = datetime.now()

    print("Reading and validating .env values...")
    configjson = json.loads(json.dumps(dotenv_values(".env")))
    sourcedir = configjson.get("SOURCE_DIRECTORY")
    targetdir = configjson.get("TARGET_DIRECTORY")
    targetcontainer = configjson.get("TARGET_FILETYPE")
    
    try:
        if (None in [sourcedir,targetdir,targetcontainer]):
            raise ValueError(".env file is malformed: can't read expected values. Check your .env file.")
        
        if (not os.path.isdir(sourcedir)):
            raise excepts.InvalidDirectoryException(f"Source directory \"{sourcedir}\" is not a valid path.")
        if (not os.path.isdir(targetdir)):
            raise excepts.InvalidDirectoryException(f"Target directory \"{targetdir}\" is not a valid path. Create an empty target directory before running the script.")
        if sourcedir == targetdir:
            raise excepts.InvalidDirectoryException(f"Target and source directories cannot be the same path.")
        
        if (targetcontainer not in ffmpeg_audiocontainers):
            raise excepts.InvalidFileFormatException(f"Target file format \"{targetcontainer}\" is not an audio file format supported by ffmpeg.")
    
        audiofilestoconvert = 0
        audiofilestomove = 0
        for (sourcepath, dirs, files) in os.walk(sourcedir):
            for file in files:
                if isAudioFile(file):
                    if getExtension(file) == targetcontainer:
                        audiofilestomove+=1
                    else:

                        audiofilestoconvert+=1
        if audiofilestoconvert+audiofilestomove==0:
            raise excepts.InvalidDirectoryException(f"Directory \"{sourcedir}\" doesn't contain any audio files!")
    
    except Exception as e:
        print(f"There was an error with the values in the .env file: {e}\nCheck your .env file.")
        raise SystemExit(1)
    
    print(".env values validated.")
    print(f"Found a total of {audiofilestoconvert+audiofilestomove} audio files, {audiofilestomove} of which are already in the desired target format.")
    timedelta = datetime.now() - timetostartpreparations
    print(f"Preparations took {round(timedelta.microseconds/1000000,5)} seconds.\n")
        
    # =====================
    # File conversion loop
    # =====================

    print(f"Starting to convert files...\n")

    timetostartfullprocess = datetime.now()
    fileintervaltoprint = math.ceil(int(audiofilestoconvert/100)) # Give 100 status updates to the user during the process
    filesconverted = 0 
    averagefileconversionlength = 0 
    remainingconversions = audiofilestoconvert

    for (sourcepath, dirs, files) in os.walk(sourcedir):

        #Copy each encountered folder to target
        targetpath = Path(sourcepath.replace(sourcedir,targetdir))
        try:
            os.makedirs(targetpath)
        except FileExistsError:
            pass
            #print(f"Directory \"{targetpath}\" already exists.")
        except PermissionError:
            print(f"Permission denied: cannot create target path \"{targetpath}\".")
            raise
        except Exception as e:
            print(f"Uncaught error occurred: {e}")
            raise

        for file in files:

            if file.startswith("."):
                continue

            fullpath = os.path.join(sourcepath,file)
            targetpath = fullpath.replace(sourcedir,targetdir)
            if not isAudioFile(file) or getExtension(file) == targetcontainer:
                copyFileToTarget(fullpath,targetpath)
                continue

            conversionstartTime = datetime.now()
            didoperation = transcodeAudioToTarget(fullpath,targetpath,targetcontainer)
            conversiontime = (datetime.now() - conversionstartTime).microseconds
            if didoperation:
                filesconverted += 1
                averagefileconversionlength = calculateNewAverage(averagefileconversionlength,filesconverted,conversiontime)

            remainingconversions -= 1

            if filesconverted > 0 and filesconverted%fileintervaltoprint==0:
                conversiontimethusfar = (datetime.now() - timetostartfullprocess).seconds
                estimatedremainingmicroseconds = remainingconversions*averagefileconversionlength
                percentageready = round(float(100-(remainingconversions/audiofilestoconvert*100)),2)
                print(f"Converted {percentageready}% of files in {round(float(conversiontimethusfar/60),2)} minutes. Estimated time remaining: {round(float(estimatedremainingmicroseconds/1000000/60),2)} minutes.")

    timeforfullprocess = (datetime.now() - timetostartfullprocess).seconds 
    hours = timeforfullprocess / 3600
    hoursremainder = timeforfullprocess % 3600
    minutes = hoursremainder / 60
    seconds = hoursremainder % 60
    print(f"Library converted in {hours} hours, {minutes} minutes and {seconds} seconds.")

if __name__ == "__main__" :
    main(sys.argv)