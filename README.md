# PhotoOrganizer

A Python toolkit to organize personal photos and videos for Windows

## Overview

Photos and videos are hard to manage, especially if you like to take a lot. You often

This toolkit provide the following tools:

### Batch Rename

### Library Management

### Deduplication

## Instructions

1. Copy photos and videos into `E:\OneDrive\Photo Library\Incoming`

1. Open cmd.exe and go to `E:\OneDrive\Photo Library`

1. Run `python E:\Code\PhotoOrganizer\photo_organizer.py setup` to rehash existing files in library

1. [Optional] Run `python E:\Code\PhotoOrganizer\photo_organizer.py audit` to check for anomalies

1. Run `python E:\Code\PhotoOrganizer\photo_organizer.py merge` to merge files into library
   - Check warning logs to analyze potential issues
   - Wait for processing and confirmation and input "y" to start the merge

## Get Started

- Copy `exiftool.exe` to working dir

## Q&A

### What files are supported?

- Photo: jpg, heic
- Video: mp4

### Development notes

- Run tests with coverage: `python .\tools\test_cov.py`
- Perf: `python .\tools\perf.py`
- Venv: `.\venv\Scripts\Activate.ps1`

- Date EXIF Observation
  - Nikon camera
    - For `.jpg` photo, `EXIF:DateTimeOriginal` is local time without timezone
    - For `.mov` video, `QuickTime:MediaCreateDate` is local time without timezone
    - `MakerNotes:TimeZone` is timezone which follows system setting and won't be auto adjusted
  - iPhone
    - For `.heic` photo, `EXIF:DateTimeOriginal` is local time without timezone, `EXIF:OffsetTime` is timezone
    - For `.mov` video, `QuickTime:CreationDate` is local time with timezone, while other `QuickTime:*` are all UTC time
      - If modified, `QuickTime:MediaCreateDate` remains unchanged, while other `QuickTime:*` will change
    - timezone will be auto adjusted
  - OnePlus phone
    - For `.jpg` photo, the fime name is local time without timezone, so is `EXIF:DateTimeOriginal`
    - For `.mp4` video, the fime name is local time without timezone, while all `QuickTime:*` are UTC time
    - timezone will be auto adjusted

### Findings

221114

- Some portrait photos are corrupted like 20211126_115753_01.heic. Only happening to portrait photos though..
- The date time provided by OneDrive is incorrect. It's likely the UTC date. This need to be fixed by not using the file name anymore
