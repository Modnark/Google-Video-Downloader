import requests
import urllib.parse as urlparse
import os
from urllib.parse import parse_qs
from helpers import downloadVideo, makeDir, threadline

docid = input("Enter docid (or filename that has docids): ")
mode = 0 if not os.path.exists(docid) else 1
rootPath = "FromID"
makeDir(rootPath)
makeDir(f"{rootPath}\\Videos")

def IsURL(string):
    parsed = urlparse.urlparse(string)
    if not parsed.scheme:
        return False
    return True

def tryDownload(docid):
    URL = f"http://web.archive.org/web/20111229082017im_/{docid}"
    if not IsURL(docid):
        URL = f"http://web.archive.org/web/20111229082017im_/http://video.google.com/videoplay?docid={docid}"
    req = requests.get(URL)
    if req.status_code == 200:
        print(f"Found page for {docid}")
        downloadVideo(req.text, URL, rootPath)
    else:
        print(f"Failed for: {docid} because: {req.status_code}") 
        
def worker(lines):
    for line in lines:
        tryDownload(line)
try:
    from bs4 import BeautifulSoup
except ImportError as e:
    print("[Warning] BS4 not found. You will not be able to save videos with titles as their names.")

if mode == 0:
    tryDownload(docid)

if mode == 1:
    threadC = input("# Threads (default: 5): ")
    threads = int(threadC) if threadC.isnumeric() and threadC and len(threadC) > 0 else 5
    threadline(open(docid, "r").readlines(), threads, worker)
