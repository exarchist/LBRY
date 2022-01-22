import os
import requests
import json
import subprocess
import sys
import glob
import argparse

#==========================================================================

# Define Global Variables

# Root Path to Process
GFilePath = ""

# Extension of the file we will upload.
GUploadFileExtension = ""

# Full FileName of the file we will upload (e.g. Video.mp4)
GUploadFileName = ""

# Full FileName of our thumbnail (e.g. Thumbnail.webp)
GThumbnailFileName = ""

# Full URL of our Thumbnail after upload
GThumbnailFileURL = ""

# Full URL we will Publish our File to
GPublishURL = ""

# Display Title of our Publish
GPublishTitle = ""

# Channel ID (Claim ID) of the Channel we will publish to
GChannelID = ""

# Channel Name (@MyAwesomeChannel) of the Channel we will publish to
GChannelName = ""

# Upload Description File
GDescriptionFile = ""

# Description Data
GDescription = ""

# Tag File
GTagFile = ""

# Tag Data
GTags = []

# Language of your content, using RFC 5646 format, eg: for English `en`, for Spanish (Spain) `es-ES`, for Spanish (Mexican) `es-MX` etc.
GLanguageID = []

GFileTypes = ["Upload", "Thumbnail", "Description", "Tag"]
GUploadFileExtension = ["mp4", "mkv", "mov", "png", "jpg", "gif", "webp", "xml", "txt", "pdf"]
GThumbnailFileExtension = ["webp", "gif", "jpg", "jpeg", "png"]
GDescriptionFileExtension = ["txt", "description"]
GTagFileExtension = ["tag", "tags"]

#==========================================================================

def SetupArgumentParser():
#
    Parser = argparse.ArgumentParser()
    Parser.add_argument("-p","--path", required=True, help="Path to File")
    Parser.add_argument("-e", "--extension", help="File Extension for the File-to-Upload (e.g. mp4)")
    Parser.add_argument("-f","--file", help="FileName")
    Parser.add_argument("-c","--channel", required=True, help="Channel ID")
    Parser.add_argument("-l","--language", required=False, help="Language of content in RFC 5646 format (e.g. en, de, es-ES,es-MX, etc.) Default: en")

    return Parser
#

#==========================================================================

def IsValidExtension(inFileType, inExtension):
#
    print(f"Searching for extension for FileType:({inFileType})")

    # Different File Types may have different valid file extensions
    if (inFileType == GFileTypes[0]):
    #
        print(f"{inExtension} in list {GUploadFileExtension}")
        return inExtension in GUploadFileExtension
    #
    elif (inFileType == GFileTypes[1]):
    #
        print(f"{inExtension} in list {GThumbnailFileExtension}")
        return inExtension in GThumbnailFileExtension
    #
    elif (inFileType == GFileTypes[2]):
    #
        print(f"{inExtension} in list {GDescriptionFileExtension}")
        return inExtension in GDescriptionFileExtension
    #
    elif (inFileType == GFileTypes[3]):
    #
        print(f"{inExtension} in list {GTagFileExtension}")
        return inExtension in GTagFileExtension
    #
    else:
    #
        return True
    #
#

#==========================================================================

def InitializeFilePath(inFilePath):
#
    global GFilePath
    GFilePath = inFilePath
#

#==========================================================================

def InitializeUploadFileExtension(inExtension):
#
    global GFilePath
    global GUploadFileExtension
    global GUploadFileName

    if (inExtension is None):
    #
        # Try to find a matching file with our list of Uploadable file extensions
        for Extension in GUploadFileExtension:
        #
            DeducedFileName = DeduceFileNameFromExtension(GFilePath, Extension)
            if (DeducedFileName is not None):
            #
                print(f"No Upload File extension specified, defaulting to: {Extension}")
                GUploadFileExtension = Extension
                GUploadFileName = DeducedFileName
                break
            #
        #
    #
    elif (IsValidExtension(GFileTypes[0], inExtension)):
    #
        GUploadFileExtension = str(inExtension)
    #
    else:
    #
        print("Error, invalid extension specified. Aborting publish...")
        sys.exit()
    #
#

#==========================================================================

# Get the File Name from Extension
def DeduceFileNameFromExtension(inPath, inExtension):
#
    # Find all Files in our path matching given extension
    FoundFiles = glob.glob(inPath + "/*." + inExtension)
    
    if (FoundFiles is not None):
    #
        NumFiles = len(FoundFiles)

        if (NumFiles > 1):
        #
            print(f"Warning: Found more than one file with specified extension ({inExtension}). Defaulting to first.")
        #
        
        if (NumFiles > 0):
        #
            outFile = FoundFiles[0]
            print(f"Found file: {outFile}")
            return outFile
        #
    #
#

#==========================================================================

# Get the File Name from Extension
def DeduceFileNameFromExtensionAbortable(inPath, inExtension):
#
    # Find all Files in our path matching given extension
    FoundFiles = glob.glob(f"{inPath}/*.{inExtension}")
    NumFiles = len(FoundFiles)

    if (NumFiles > 1):
    #
        print(f"Warning: Found more than one file with specified extension ({inExtension}). Defaulting to first.")
    #
    elif (NumFiles < 1):
    #
        print(f"Error: No file found with specified extension ({inExtension})! Aborting...")
        sys.exit()
    #

    outFile = FoundFiles[0]
    print("Found file: " + outFile)
    return outFile
#

#==========================================================================

def InitializeUploadFileData(inFileExtension, inFileName):
#
    global GFilePath
    global GUploadFileExtension
    global GUploadFileName

    GUploadFileName = inFileName
    
    # Initialize our Upload FileExtension
    InitializeUploadFileExtension(inFileExtension)

    if (GUploadFileName is None):
    #
        # Get our Upload's filename if not specified yet
        GUploadFileName = DeduceFileNameFromExtension(GFilePath, GUploadFileExtension)
    #
#

#==========================================================================

def InitializeChannelID(inChannelID):
#
    global GChannelID
    GChannelID = inChannelID
#

#==========================================================================

def InitializeChannelName(inChannelName):
#
    global GChannelName
    GChannelName = inChannelName
#

#==========================================================================

def InitializeLanguageID(inLanguageID):
#
    global GLanguageID
    GLanguageID = inLanguageID
#

#==========================================================================

def InitializeChannelData(inChannelData):
#
    if (inChannelData):
    #
        # Distinguish between ChannelID and ChannelName
        if (inChannelData[0] == "@"):
        #
            # We found a ChannelName
            InitializeChannelName(inChannelData)
        #
        else:
        #
            # We found a ChannelID
            InitializeChannelID(inChannelData)
        #
    #
    else:
    #
        print("Channel Data missing. Aborting publish...")
        sys.exit()
    #
#

#==========================================================================

def InitializeThumbnail(inPath):
#
    global GThumbnailFileName
    GThumbnailFileName = DeduceThumbnailName(inPath)

    if (GThumbnailFileName is None):
    #
        print("TODO!")
        #if (GGenerateThumbnail is True):
        #
            # TODO Generate
        #
    #
#

#==========================================================================

def DeduceThumbnailName(inPath):
#
    outFile = ""
    for Extension in GThumbnailFileExtension:
    #
        outFile = DeduceFileNameFromExtension(inPath, Extension)

        if (outFile is not None):
        #
            break
        #
    #
    return outFile
#

#==========================================================================

def UploadThumbnail(inPath, inThumbName):
#
    global GThumbnailFileURL
    
    print(f"Uploading Thumbnail File: {inThumbName}")

    # Preparing json to send to spee.ch
    thumbnailParams = \
    {
        "name": inThumbName
    }
    files = \
    {
        'file': open(inThumbName,'rb')
    }
    
    print("Uploading thumbnail to spee.ch...\n")
    reqResult = requests.post("https://spee.ch/api/claim/publish", files=files,data=thumbnailParams)
    
    # Process response from spee.ch api
    if (reqResult.status_code == 200):
    #
        returnJson = reqResult.json()
        print(f"Finish upload thumbnail, result json: {json.dumps(returnJson)}\n")

        # Set our global value for the URL
        GThumbnailFileURL = returnJson["data"]["serveUrl"]
    #
    else:
    #
        print(f"Spee.ch error: {reqResult.text}\nAborting...")
        sys.exit()
    #
#

#==========================================================================

def InitializeDescription(inPath):
#
    global GDescriptionFile
    global GDescription

    GDescriptionFile = DeduceDescriptionFile(inPath)
    print(f"Looking for Description in file: {GDescriptionFile}")

    if (GDescriptionFile is not None):
    #
        ReadFile = open(GDescriptionFile, 'r', encoding='utf-8-sig').read()
        GDescription = str(ReadFile)

        if (GDescription is not None):
        #
            print(f"Description read in from file: {GDescriptionFile}")
            print(f"Description: {GDescription}")
        #
    #
#

#==========================================================================

def DeduceDescriptionFile(inPath):
#
    outFile = ""
    for Extension in GDescriptionFileExtension:
    #
        outFile = DeduceFileNameFromExtension(inPath, Extension)

        if (outFile is not None):
        #
            break
        #
    #
    return outFile
#

#==========================================================================

def InitializeTags(inPath):
#
    global GTags
    GTagFile = DeduceTagFile(inPath)
    print(f"Looking for Tags in file: {GTagFile}")

    if (GTagFile is not None):
    #
        Count = 0
        ReadFile = open(GTagFile).readlines()
        for Line in ReadFile:
        #
            if (Count < 5):
            #
                GTags.append(Line.strip("\n"))
                Count = Count + 1
            #
        #
    #
    print(f"Tags read in from file: {GTags}")
#

#==========================================================================

def DeduceTagFile(inPath):
#
    outFile = ""
    for Extension in GTagFileExtension:
    #
        outFile = DeduceFileNameFromExtension(inPath, Extension)

        if (outFile is not None):
        #
            break
        #
    #
    return outFile
#

#==========================================================================

def InitializePublishURL():
#
    global GPublishURL

    print(f"Publishing GUploadFileName: {GUploadFileName}")

    # Trim Path information from Filename
    FilenameNoPath = os.path.basename(GUploadFileName)
    # Trim Extension from Filename
    FilenameNoExtension = FilenameNoPath.rsplit(".", 1)[0]
    # Clean special characters, underscores and spaces from Filename
    specialChars = " []_"
    for specialChar in specialChars:
        FilenameNoExtension = FilenameNoExtension.replace(specialChar, "-")
    GPublishURL = FilenameNoExtension

    print(f"Publishing to URL: {GPublishURL}")
#

#==========================================================================

def InitializePublishTitle():
#
    global GPublishTitle

    # Trim Path information from Filename
    FilenameNoPath = os.path.basename(GUploadFileName)
    # Trim Extension from Filename
    FilenameNoExtension = FilenameNoPath.rsplit(".",1)[0]
    # Clean Underscores from Filename
    # FilenameCleaned = FilenameNoExtension.replace("_"," ")

    # Built-in Python Title uppercasing
    GPublishTitle = FilenameNoExtension

    print(f"Publishing with Title: {GPublishTitle}")
#

#==========================================================================

def ConstructJSON():
#
    # Prepare json to send to lbrynet api
    OutJSON = \
    {
        "method": "publish",
        "params": \
        {
            # Name (corresponds to the URL. Cannot contain spaces!)
            "name": GPublishURL,
            # Title (corresponds to the View Title)
            "title" : GPublishTitle,
            "bid": "0.01",
            # Source File (full path)
            "file_path": GUploadFileName,
            "validate_file": False,
            "optimize_file": False,
            "description": GDescription,
            "tags": GTags,
            # Channel's Name (e.g. @MyAwesomeChannel)
            "channel_name": GChannelName,
            # Channel's Claim ID (e.g. b1ff6c2746a91860188b676b674083c6379d3a49)
            "channel_id": GChannelID,
            "languages": GLanguageID,
            "locations": [],
            "thumbnail_url": GThumbnailFileURL,
            "funding_account_ids": [],
            "preview": False,
            "blocking": False
        }
    }
    return OutJSON
#

#==========================================================================

def Publish(inJSON):
#
    print(f"Uploading file with parameters: {json.dumps(inJSON)}\n")

    PublishResult = requests.post("http://localhost:5279/",json.dumps(inJSON))

    if (PublishResult.status_code == 200):
    #
        returnJson = PublishResult.json()
        print(f"Finish uploading file, result json: " + json.dumps(returnJson) + "\n")
    #
    else:
    #
        print(f"Error uploading file: {PublishResult.text}\n")
    #
#

#==========================================================================
#==========================================================================
#==========================================================================


# Setup our Argument Parser
Parser = SetupArgumentParser()
# Parse our CommandLine arguments
args = Parser.parse_args()

# Initialize our Path
InitializeFilePath(args.path)

# Initialize our UploadFile
InitializeUploadFileData(args.extension, args.file)

# Initialize our Channel data
InitializeChannelData(args.channel)

# Initialize our language data
InitializeLanguageID(args.language)

# Initialize our Thumbnail
InitializeThumbnail(GFilePath)

# Upload our Thumbnail to Speech Server
UploadThumbnail(GFilePath, GThumbnailFileName)

# Initialize our Description
InitializeDescription(GFilePath)

# Initialize our Tags
InitializeTags(GFilePath)

# Initialize Publish URL
InitializePublishURL()

# Initialize Publish Title
InitializePublishTitle()

# Initialize Publish JSON
PublishJSON = ConstructJSON()

# Publish our File
Publish(PublishJSON)
