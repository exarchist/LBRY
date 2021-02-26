# LBRY

A collection of tools for interacting with the LBRY service

LBRY is an excellent service, but due to its immaturity lacks many key features that discourage creators from adopting it.

The aim is to create tools which are:

* Functional
* Well-Documented
* Accessible

Comments and contributions welcome.

# Optimize-Video

A tool to optimize a given video file for LBRY recommended settings.

## Dependencies

* Python 3.X
* FFMPEG (2021-01-09-git-2e2891383e-full_build-www.gyan.dev)

## Usage

Within a commandline or Powershell window:
```py.exe .\optimize-video.py -input C:\Path\To\InputVideo.mp4```
optionally:
```py.exe .\optimize-video.py -input C:\Path\To\InputVideo.mp4 -output C:\Path\To\OutputVideo.mp4```

### Parameters

* -input or -i
* -output or -o
