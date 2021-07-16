import re
import os
import urllib
import requests
from threading import Thread

canUseBS4 = True
valid_chars = '_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&-+='

try:
    from bs4 import BeautifulSoup
except ImportError as e:
    canUseBS4 = False

# This function was written by NT_x86
def threadline(list,numthreads,function):
	threadlists = {}

	#make lists
	for x in range(numthreads):
		threadlists["thread"+str(x)] = []
		thrdnum = 0
        
	#append all the lines to lists
	for line in list:
		threadlists["thread"+str(thrdnum)].append(line)
		if thrdnum == numthreads-1:
			thrdnum = 0
		else:
			thrdnum = thrdnum+1

	#run the threads
	for x in range(numthreads):
		Thread(target=function, args=(threadlists["thread"+str(x)], )).start()

# Make a directory
def makeDir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)    

# Filter file names
def getfilteredname(name):
	fname = ''.join(c for c in name if c in valid_chars)
	return fname

# Download a video
def downloadVideo(html, vidName, rootPath):
    # Make paths
    makeDir(f"{rootPath}\\Success")
    makeDir(f"{rootPath}\\Failed")
    makeDir(f"{rootPath}\\Videos")

    soup = BeautifulSoup(html, features='html.parser')
    vidTitle = soup.find("div", {"id": "video-title"})

    vidName = f"{rootPath}\\Videos\\{vidName}.flv" if not vidTitle else f"{rootPath}\\Videos\\{getfilteredname(f'{vidTitle.getText()}')}.flv"
    mobj = re.search(r"(?i)videoUrl\\x3d(.+?)\\x26", html)

    if mobj is None:
        print("FAILED TO FIND VIDEO")
    else:
        mediaURL = urllib.parse.unquote(mobj.group(1))
        mediaURL = mediaURL.replace('\\x3d', '\x3d')
        mediaURL = mediaURL.replace('\\x26', '\x26')

        req = requests.get(f"http://web.archive.org/web/20110418212702im_/{mediaURL}", allow_redirects=True)
        URL = req.url + "\n"
        if not URL in open(f"{rootPath}\Success\\Success.txt", "a+").read():
            if req.status_code == 200:
                print(f"Successfully downloaded {vidName}")
                with open(f"{rootPath}\\Success\\Success.txt", "a+") as good:
                    good.write(URL)
                with open(vidName, "wb+") as video:
                    video.write(req.content)
            else:
                print(f"Failed to download {vidName} becasue: {req.status_code}")
                if not URL in open(f"{rootPath}\\Failed\\{req.status_code}.txt", "w+").read():
                    with open(f"{rootPath}\\Failed\\{req.status_code}.txt", "a+") as stcode:
                        stcode.write(URL)  