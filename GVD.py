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

def getDocIdFromURL(url):
    parsed = urlparse.urlparse(url.split(" ")[0])
    if not parsed.scheme:
        return False
    try:
        return parse_qs(parsed.query)['docid'][0]
    except Exception as e:
        return False

def worker(lines):
    for line in lines:
        if not getDocIdFromURL(line) == False:
            line = getDocIdFromURL(line)
        req = requests.get(f"http://web.archive.org/web/http://video.google.com/videoplay?docid={line.strip().lstrip()}")
        if req.status_code == 200:
            print(f"Found page for {line.strip().lstrip()}")
            downloadVideo(req.text, line.strip().lstrip(), rootPath)
        else:
            print(f"Failed for: {line.strip().lstrip()} because: {req.status_code}")

try:
    from bs4 import BeautifulSoup
except ImportError as e:
    print("[Warning] BS4 not found. You will not be able to save videos with titles as their names.")

if mode == 0:
    if not getDocIdFromURL(docid) == False:
        docid = getDocIdFromURL(docid)
    req = requests.get(f"http://web.archive.org/web/http://video.google.com/videoplay?docid={docid}")
    if req.status_code == 200:
        print(f"Found page for {docid}")
        downloadVideo(req.text, docid, rootPath)
    else:
        print(f"Failed for: {docid} because: {req.status_code}") 

if mode == 1:
    threadC = input("# Threads (default: 5): ")
    threads = int(threadC) if threadC.isnumeric() and threadC and len(threadC) > 0 else 5
    threadline(open(docid, "r").readlines(), threads, worker)
