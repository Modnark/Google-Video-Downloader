# Google Videos Downloader
A tool that utilizes archive.org to download old videos from google video.

## Special thanks to
NT_x86 for some of the functions, and for his method of downloading videos.
archive.org for their amazing service for digital preservation
an old version of youtube-dl for some regex patterns

# Setup
You will need:
The latest version of Python (get it [here](https://python.org))
The requests module (install with pip)
The bs4 module (install with pip)

# Usage
```py .\GVD.py```

You can download a single video by entering its docid, or multiple videos at once by entering a filename.

Single video:
```
Enter docid (or filename that has docids): YOURVIDEODOCID
```

Multiple videos:
```
Enter docid (or filename that has docids): Videos.txt
```

When downloading multiple videos you will be asked for the number of threads, just press enter for the default (5) or enter a higher number, though be warned, archive.org may rate limit or temporarily suspend access to their services if the number is too high.
