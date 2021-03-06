import os
import sys
import subprocess
import pathlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input", required=True, help="Full Path to Video File (e.g. C:\Path\To\Input.mp4)")
parser.add_argument("-q","--quality", type=int, help="Quality Metric (0 = Best, No Loss, 23 = Good, Some Loss, 51 = Bad, Very Lossy). Defaults to 29")
parser.add_argument("-o","--output", help="If specified, Full Path and Output Filename (e.g. C:\Path\To\Output.mp4)")
args = parser.parse_args()

# Input File Name (requires Full Path)
InputFile = args.input

if (InputFile is None):
#
    # If no Input File is specified, we have nothing to do.
    print("Missing input file! Aborting operation ...")
    sys.exit()
#

# Get the Path where the Input File resides
FilePath = os.path.dirname(InputFile)

# Get the InputFile Name without the path
InputFileName = os.path.basename(InputFile)
print(f"Processing {InputFileName}...")

# Initialize Quality
Quality = args.quality
if (Quality is not None):
#
    if (Quality < 0 or Quality > 51):
    #
        print("Invalid quality value specified.")
        if (input("Would you like to continue with a default quality? [y/N]") != "y"):
        #
            sys.exit()
        #
    #
#

if (Quality is None or Quality < 0 or Quality > 51):
#
    # Use a default Quality value
    Quality = 29
#
print(f"Output video quality is {Quality}")

# Output File Name (if specified via Parameter)
OutputName = args.output

# If no Output File Name, assign a default
if (OutputName is None):
#
    OutputName = f"{FilePath}/Output_{Quality}.mp4"
#
print(f"Output file will be {OutputName}...")

# Specify our Codec
Codec = "libx264"

# Use MovFlags w/ FastStart to ensure MP4 header info is written at the start of the file
MovFlags = "-movflags +faststart"

convertCommand = f"ffmpeg -i {InputFile} -c:a copy -c:v {Codec} -crf {Quality} -maxrate 500K -bufsize 500K -rc:v vbr_hq -shortest {MovFlags} {OutputName}" 

print("\n" + convertCommand + "\n")
subprocess.call(convertCommand)
