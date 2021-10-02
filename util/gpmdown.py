from typing import Sequence
import requests
from multiprocessing.pool import ThreadPool
# from requests.sessions import Session, session
from os.path import exists

from requests.api import head

headers = {
    'Accept-Encoding': 'gzip',
    'Accept-Language': 'en-US,en;q=0.5',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.06',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Cache-Control': 'max-age=0',
    'Connection': 'Keep-Alive',
}

def download_url(url):
  # assumes that the last segment after the / represents the file name
  # if url is abc/xyz/file.txt, the file name will be file.txt
    file_name_start_pos = url.rfind("/") + 1
    file_name_end_pose = url.find("?")
    file_name = url[file_name_start_pos:file_name_end_pose]

    if not exists(file_name):
        print("downloading: ",url)
        r = requests.get(url, stream=True, headers=headers)
        if r.status_code == requests.codes.ok:
          with open(file_name, 'wb') as f:
            for data in r:
              f.write(data)
        return url

def main(link_list):
    # Get the urls from the txt file as a list using readline
    file1 = open(link_list, 'r')
    Lines = file1.readlines()

    urls = []
    count = 0
    # Strips the newline character
    for line in Lines:
        count += 1
        urls.append(line.strip())

    # Run 5 multiple threads. Each call will take the next element in urls list
    results = ThreadPool(4).imap_unordered(download_url, urls)
    for r in results:
        print(r)

if __name__ == "__main__":
    main()