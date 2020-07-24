import urllib.request
from bs4 import BeautifulSoup
from time import sleep
import json
import hashlib
import os
from PIL import Image
import glob

files = glob.glob("../../docs/files/**/*.jpg", recursive=True)

for i in range(len(files)):
    print(i, len(files), files[i])

    file = files[i]
    dirname = os.path.dirname(file)
    odirname = dirname.replace("/original/", "/medium/")

    os.makedirs(odirname, exist_ok=True)

    ofile = file.replace("/original/", "/medium/")

    if not os.path.exists(ofile):

        img = Image.open(file)

        img_resize = img.resize((256,round(img.height * 256 / img.width)))
        img_resize.save(ofile)

