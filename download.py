import urllib.request
import requests
import codecs
import re
import shutil
import os
from zipfile import ZipFile
from text import direct_download_link_pattern, direct_download_page

global current_path

def start_direct_download(dest_path) -> int:
    global current_path
    current_path = dest_path
    page = urllib.request.urlopen(direct_download_page)
    html = page.read()
    page.close()
    html = codecs.ascii_decode(html, "ignore")[0]
    matches = re.findall(pattern=direct_download_link_pattern, string=html)
    if len(matches) <= 0:
        return -1
    if download_and_save_file(matches[0]) < 0:
        return -1
    return 1

def download_and_save_file(url) -> int:
    download(url)
    try:
        ZipFile(f"{current_path}/temp.zip",mode='r').extract(member="chromedriver-win64/chromedriver.exe",path=current_path)
        shutil.move(f"{current_path}/chromedriver-win64/chromedriver.exe", f"{current_path}/chromedriver.exe")
        os.removedirs(f"{current_path}/chromedriver-win64")
        os.remove(f"{current_path}/temp.zip")
        return 0
    except:
        return -1

def download(url) -> int:
    file_path = os.path.join(current_path, "temp.zip")

    r = requests.get(url, stream=True)
    
    if r.ok:
        download_size = 0
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 128):
                if chunk:
                    download_size += f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
            return download_size
    else:  # HTTP status code 4xx/5xx
        return -1
