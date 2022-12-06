import shutil
import requests
import re
import csv
import os

acceptable_extensions = {'zip','tar','gztar','bztar','xztar'}

def download_songs(file_urls):
    total_files = len(file_urls)
    for i, file in enumerate(file_urls):
        #Process URLS
        file_name = file.split('/')[-1]
        file_path = os.path.join(zip_path, file_name)

        if file_name.split('.')[-1] not in acceptable_extensions:
            print(f'[{i+1} of {total_files}] Skipped {file}')
            continue
        
        if os.path.exists(file_path):
            print(f'[{i+1} of {total_files}] {file_name} already exists')
            continue

        #Download Zip Files into zip_path
        req = requests.get(file)
        if req.status_code == 200:
            with open(file_path, 'wb') as handler:
                file_data = req.content
                handler.write(file_data)
                print(f'[{i+1} of {total_files}] Downloaded {file_name}')
        else:
            print(f'[{i+1} of {total_files}] Error Downloading {file_name}, response {req.status_code}')
            continue
            
        #Extract and Organize Zip Files into songs_path
        ext_path = os.path.join(songs_path, file_name.split('.')[0])
        try:
            shutil.unpack_archive(file_path, ext_path)
        except:
            print(f'Could not extract {file_name}')

def find_csv_file():
    dir_list = os.listdir()
    for item in dir_list:
        if item.split('.')[-1] == 'csv':
            return item

def detect_url(string):
        # findall() has been used 
        # with valid conditions for urls in string
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex,string)      
        return [x[0] for x in url]



file_urls = []

songs_list_file = find_csv_file()

with open(songs_list_file, newline='', encoding='utf8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        for col in row:
            url = detect_url(col)
            if url != []:
                file_urls.append(url[0])

zip_path = './zip_files'
songs_path = './songs'

os.makedirs(zip_path, exist_ok=True)
os.makedirs(songs_path, exist_ok=True)

input(f'{len(file_urls)} songs found! Press [enter] to begin downloading...')
download_songs(file_urls)

