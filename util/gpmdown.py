############### ASYNC DOWNLOAD #############

import requests
from multiprocessing.pool import ThreadPool
import os
import time

headers = {
    'Accept-Encoding': 'gzip',
    'Accept-Language': 'en-US,en;q=0.5',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.06',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Cache-Control': 'max-age=0',
    'Connection': 'Keep-Alive',
}

def download_url(url):
    # print("downloading: ", url)
    # assumes that the last segment after the / represents the file name
    # if url is abc/xyz/file.txt, the file name will be file.txt
    file_name_start_pos = url.rfind("/") + 1
    file_name_end_pos = url.find("?")
    fname = url[file_name_start_pos:file_name_end_pos]

    if not os.path.exists(fname):
        s = requests.Session()
        s.max_redirects = 80
        r = s.get(url, stream=False, allow_redirects=True, headers = headers, timeout = 1000)
        if r.status_code == requests.codes.ok:
          with open(fname, 'wb') as f:
            for data in r:
              f.write(data)
        print("downloaded and saved : " + fname)
        time.sleep(5)
        return url

def down(year):
    # Get the urls from the txt file as a list using readline
    file1 = open("../text_files/" + year + ".txt", 'r')
    Lines = file1.readlines()

    urls = []
    count = 0
    # Strips the newline character
    for line in Lines:
        count += 1
        urls.append(line.strip())

    # Run 5 multiple threads. Each call will take the next element in urls list
    results = ThreadPool(25).imap_unordered(download_url, urls)
    for r in results:
        # print(r)
        pass

    print("COMPLETE: downloaded all files in the list")


############# BASIC DOWNLOAD ###########
# import requests
# import os

# def down(year):
#     # Get the urls from the txt file as a list using readline
#     file1 = open("../text_files/" + year + ".txt", 'r')
#     Lines = file1.readlines()

#     urls = []
#     count = 0
#     # Strips the newline character
#     for line in Lines:
#         count += 1
#         urls.append(line.strip())

#     for url in urls:
#     # Set the FILENAME string to the data file name, the LABEL keyword value, or any customized name.
#         file_name_start_pos = url.rfind("/") + 1
#         file_name_end_pos = url.find("?")
#         fname = url[file_name_start_pos:file_name_end_pos]

#         if not os.path.exists(fname):
#             result = requests.get(url)
#             try:
#                result.raise_for_status()
#                f = open(fname,'wb')
#                f.write(result.content)
#                f.close()
#                print('contents of URL written to '+ fname)
#             except:
#                print('requests.get() returned an error code '+str(result.status_code))

#     print("COMPLETE: downloaded all files in the list")
