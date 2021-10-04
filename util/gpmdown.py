# import os
# import asyncio
# import aiohttp  # pip install aiohttp
# import aiofiles  # pip install aiofiles

# REPORTS_FOLDER = "reports"
# FILES_PATH = os.path.join(REPORTS_FOLDER, "files")

# async def fetch_file(url):
#     sema = asyncio.BoundedSemaphore(5)
#     file_name_start_pos = url.rfind("/") + 1
#     file_name_end_pose = url.find("?")
#     fname = url[file_name_start_pos:file_name_end_pose]

#     async with sema, aiohttp.ClientSession() as session:
#         async with session.get(url) as resp:
#             assert resp.status == 200
#             data = await resp.read()

#     async with aiofiles.open(fname, "wb") as outfile:
#         if not os.path.exists(fname):
#             await outfile.write(data)

# def main(link_list):
#     # Get the urls from the txt file as a list using readline
#     file1 = open(link_list, 'r')
#     Lines = file1.readlines()

#     urls = []
#     count = 0
#     # Strips the newline character
#     for line in Lines:
#         count += 1
#         urls.append(line.strip())

#     loop = asyncio.get_event_loop()
#     tasks = [loop.create_task(fetch_file(url)) for url in urls]
#     loop.run_until_complete(asyncio.wait(tasks))
#     loop.close()

#     print("COMPLETE: downloaded all files in the list")

# THE BASIC code
# Set the URL string to point to a specific data URL. Some generic examples are:
#   https://servername/data/path/file
#   https://servername/opendap/path/file[.format[?subset]]
#   https://servername/daac-bin/OTF/HTTP_services.cgi?KEYWORD=value[&KEYWORD=value]

import requests

def down(link_list):
    # Get the urls from the txt file as a list using readline
    file1 = open(link_list, 'r')
    Lines = file1.readlines()

    urls = []
    count = 0
    # Strips the newline character
    for line in Lines:
        count += 1
        urls.append(line.strip())

    for url in urls:
    # Set the FILENAME string to the data file name, the LABEL keyword value, or any customized name.
        file_name_start_pos = url.rfind("/") + 1
        file_name_end_pose = url.find("?")
        fname = url[file_name_start_pos:file_name_end_pose]

        result = requests.get(url)
        try:
           result.raise_for_status()
           f = open(fname,'wb')
           f.write(result.content)
           f.close()
           print('contents of URL written to '+ fname)
        except:
           print('requests.get() returned an error code '+str(result.status_code))
