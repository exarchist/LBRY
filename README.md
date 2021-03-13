# LBRY

A collection of tools for interacting with the LBRY service

LBRY is an excellent service, but due to its immaturity lacks many key features that discourage creators from adopting it.

The aim is to create tools which are:

* Functional
* Well-Documented
* Accessible

Comments and contributions welcome. Code is licensed under GPL.

----

# Publish File

A commandline tool to publish a file to LBRY, with support for automatically populating other data relevant to each published file, such as:

* Title
* URL
* Thumbnail
* Description
* Tags

## Dependencies

* Python 3.X
* FFMPEG (2021-01-09-git-2e2891383e-full_build-www.gyan.dev)

## Usage

Within a commandline or Powershell window:  
```py.exe .\publish-file.py --path C:\Path\To\Files --channel @MyAwesomeChannel```

This basic usage will direct our tool to visit the path specified. Within this path, the script expects to find several files:

* **FileToPublish**: A file you wish to publish
    * e.g. MyVideo.mp4, MyMusicFile.mp3, MyImage.png, MyBook.pdf 
* **Thumbnail**: A small image file that will be used as your thumbnail image for a given publish
    * e.g. MyThumbnail.webp, MyThumbnail.png, MyThumbnail.gif
* **Description**: A text file with information you wish to have written to the "Description" data of a given published file
    * The file extension for this file must be ".description"
    * e.g. MyDescription.description 
* **Tag**: A text file with a list of up to 5 tags
    * Each tag is on a single line
    * The file extension for this file must be ".tag" or ".tags"
    * e.g. MyTags.tags

optionally:  
```py.exe .\publish-file.py -input C:\Path\To\Files --channel @MyAwesomeChannel --extension .mp4```  
optionally:  
```py.exe .\publish-file.py -input C:\Path\To\Files --channel @MyAwesomeChannel --file SpecificFileInPath.mp4```  

### Parameters

#### Required Parameters
* --path or -p
    * Path within which the File-to-Upload can be Found. If blank, will automatically attempt to find files to upload
* --channel or -c
    * Channel Identifier e.g. @MyAwesomeChannel

#### Optional Parameters
* --file or -f
    * Filename if explicitly specifying a file to upload
* --extension or -e
    * File-extension the script will use to deduce a file to upload 

----

# Optimize-Video

A commandline tool to optimize a given video file for LBRY recommended settings.

## Dependencies

* Python 3.X
* FFMPEG (2021-01-09-git-2e2891383e-full_build-www.gyan.dev)

## Usage

Within a commandline or Powershell window:  
```py.exe .\optimize-video.py -input C:\Path\To\InputVideo.mp4```  
optionally:  
```py.exe .\optimize-video.py -input C:\Path\To\InputVideo.mp4 -output C:\Path\To\OutputVideo.mp4```  
optionally:  
```py.exe .\optimize-video.py -input C:\Path\To\InputVideo.mp4 -output C:\Path\To\OutputVideo.mp4 -quality 25```  

### Parameters

* --input or -i
    * Path to the Input File 
* --output or -o
    * Path to use for the Output File 
* --quality or -q
    * FFMPEG Quality setting to use for Optimization (0 = Best, 51 = Worst)  
