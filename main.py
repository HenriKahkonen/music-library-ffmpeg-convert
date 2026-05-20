import sys, argparse, time, json, os
import ffmpeg
import utils.exceptions as excepts
from dotenv import dotenv_values
from pathlib import Path

from utils.funcs import isAudioFile
from utils.constants import ffmpeg_audiocontainers

def main(argv: list[str]) -> int:

    parser = argparse.ArgumentParser(description="Music Library ffmpeg converter")
    parser.add_argument("--log",action="store_true",help="Use argument to log operations to .txt output")
    args = parser.parse_args(argv[1:])

    print("\n"+"="*25+"Music library converter tool"+"="*25+"\n")

    logging = args.log
    if logging:
        print("Logging: True")
        #TODO: implement    
    
    #  ================
    #  Pre-operation validations
    #  ================

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
        
        if (targetcontainer not in ffmpeg_audiocontainers):
            raise excepts.InvalidFileFormatException(f"Target file format \"{targetcontainer}\" is not an audio file format supported by ffmpeg.")
    
        sourcedir_folders = [ name for name in os.listdir(sourcedir) if os.path.isdir(os.path.join(sourcedir, name)) ]
        audiofilesfound = False
        for (root,dirs,files) in os.walk(sourcedir):
            #print(" ")
            #print(f"Root: {root}")
            #print(f"Dirs: {dirs}")
            #print(f"File: {file}")
            #time.sleep(3)
            for file in files:
                if isAudioFile(file):
                    audiofilesfound = True
                    break
            if audiofilesfound:
                break
        if not audiofilesfound:
            raise excepts.InvalidDirectoryException(f"Directory \"{sourcedir}\" doesn't contain any audio files!")
    
    except Exception as e:
        print(f"There was an error with the values in the .env file: {e}\nCheck your .env file.")
        raise SystemExit(1)
    
    print(".env values validated. Beginning to process files...\n")
    
    # =====================
    # File conversion loop
    # =====================

    for (sourcepath, dirs, files) in os.walk(sourcedir):
        # Inspect whether or not dir contains audio files
        isMusicFolder = False
        if files:
            for file in files:
                if isAudioFile(file):
                    isMusicFolder = True
                    break
            if isMusicFolder:
                targetpath = Path(sourcepath.replace(sourcedir,targetdir))
                try:
                    print(targetpath)
                    os.makedirs(targetpath)
                except FileExistsError:
                    print(f"Directory \"{targetpath}\" already exists.")
                except PermissionError:
                    print(f"Permission denied: cannot create target path \"{targetpath}\"")
                    raise
                except Exception as e:
                    print(f"Uncaught error occurred: {e}")
                    raise
                #print(targetpath)
                #print("create")


    # TODO: function that processes every file and converts to .mp3

    

    


    #except SyntaxError:
    #    print("Error: .env file is malformed. Check that your .env file is set up correctly.")
    #    sys.exit(1)

if __name__ == "__main__" :
    main(sys.argv)