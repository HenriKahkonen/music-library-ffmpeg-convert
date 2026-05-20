# Music library ffmpeg converter tool

This script is to be used to non-destructively mass-convert a music library into a desired file format, for example to a .mp3 format to be compatible with certain devices. Tool uses ffmpeg for file conversions.

Script reads a directory recursively, identifies audio files and converts them into the desired container.

# Setup and dependencies

This script is written using python 3.13.12. Some dependencies need to be installed for the conversion operations to work.

### Create venv
```
# macOS/Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```
### Install dependencies
```
pip3 install -r requirements.txt
```
### Set up your source and target files as well as your target file format
In the project's root folder is a file called _.env-example_. Create a file in the same root folder called _.env_ and copy the example envs contents to it, substituting the folders with your own.

# Using the tool

After the variables have been set, run the script with:

> python3 main.py

If you want to output a .txt log of the actions, add flag --log and run the command as:

> python3 main.py --log

The script then starts to read through the target directory. If it encounters files already in the desired file format, it copies the files into the target directory. If a file with a matching filename exists in the target directory, source file is not copied, meaning you can run the script multiple times without flooding your disk with duplicate files.

Whenever the script encounters audio files that are not in the desired output format, the file is converted to the target format using the ffmpeg library and copied to the target folder using same duplicate prevention logic as above.