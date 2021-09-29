from typing import Sequence
import requests
from multiprocessing.pool import ThreadPool

from requests.sessions import Session, session

username = "adisen99"
password = "Sai@baba99"
 
def download_url(url):
  print("downloading: ",url)
  file_name_start_pos = url.rfind("/") + 1
  file_name = url[file_name_start_pos:]

  # main download algorithm
  with requests.Session() as session:
    s.auth = (username, password)
    r1 = session.request('get', url)
    r = session.get(r1.url, auth = (username, password))

    if r.ok:
      with open(file_name, 'wb') as f:
        for data in r:
          f.write(data)
      # print r.content

  return url
 
 
# Get the urls from the txt file as a list using readline
file1 = open('myfile.txt', 'r')
Lines = file1.readlines()
 
urls = []
count = 0
# Strips the newline character
for line in Lines:
    count += 1
    urls.append(line.strip())
 
# Run 5 multiple threads. Each call will take the next element in urls list
results = ThreadPool(5).imap_unordered(download_url, urls)
for r in results:
    print(r)