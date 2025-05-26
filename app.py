from pytubefix import YouTube
from sys import argv
import os

link = argv[1]
yt = YouTube(link)

print("Title: ", yt.title)
print("Views: ", yt.views)

yd = yt.streams.get_highest_resolution()

download_folder = 'videos'

if not os.path.exists(download_folder):
    os.makedirs(download_folder)

yd.download(output_path=download_folder)

print(f'Download concluído em {download_folder}!')