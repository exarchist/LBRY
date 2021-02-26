import os
import sys
import subprocess
import pathlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input", required=True, help="Full Path to Video File (e.g. C:\Path\To\Input.mp4)")
parser.add_argument("-o","--output", help="If specified, Full Path and Output Filename (e.g. C:\Path\To\Output.mp4)")
args = parser.parse_args()

# Input File Name (requires Full Path)
inputFile = args.input

if (inputFile is None):
#
    # If no Input File is specified, we have nothing to do.
    print("Missing input file! Aborting operation ...")
    sys.exit()
#

# Get the Path where the Input File resides
filePath = os.path.dirname(inputFile)

# Get the InputFile Name without the path
inputFileName = os.path.basename(inputFile)

print(f"Processing {inputFileName}...")

# Output File Name (if specified via Parameter)
outputName = args.output

# If no Output File Name, assign a default
if (outputName is None):
#
    outputName = f"{filePath}/output.mp4"
#
print(f"Output file will be {outputName}...")

convertCommand = f"ffmpeg -i {inputFile} -c:a copy -c:v libx264 -maxrate 5000K -bufsize 5000K -rc:v vbr_hq -cq:v 19 {outputName}"
print(convertCommand)
subprocess.call(convertCommand)



