import urllib.request
from bs4 import BeautifulSoup
from time import sleep
import json
import hashlib
import os
from PIL import Image
import glob
import pandas as pd
import openpyxl

df = pd.read_csv("../data/images.csv", header=None, index_col=None)

r_count = len(df.index)
c_count = len(df.columns)

ids = {}

for j in range(1, r_count):
    id = df.iloc[j, 0]
    url = df.iloc[j, 1]

    if id not in ids:
        ids[id] = []
    
    ids[id].append(url)

prefix_url = "https://nakamura196.github.io/iriki"
prefix_path = "../../docs"

rows_0 = [
    ["ID", "Title", "Thumbnail", "manifest", "viewingDirection", "Relation", "viewingHint", "rights", "attribution"],
    ["http://purl.org/dc/terms/identifier", "http://purl.org/dc/terms/title", "http://xmlns.com/foaf/0.1/thumbnail", "http://schema.org/url", "http://iiif.io/api/presentation/2#viewingDirection", "http://purl.org/dc/terms/relation", "http://iiif.io/api/presentation/2#viewingHint", "http://purl.org/dc/terms/rights", ""],
    ["Literal", "Literal", "Resource", "Resource", "Resource", "Resource", "Resource", "Resource", "Literal"],
    ["", "", "", "", "", "", ""],
]

rows_1 = [
    ["ID", "Thumbnail"]
]

rows_2 = [
    ["ID", "Original", "Thumbnail", "Width", "Height"]
]

rows_3 = [
    ["label", "url"],
    ["入来院文書", prefix_url+"/iiif/collection/top.json"]
]

for id in ids:
    urls = ids[id]

    thumbnail_url_0 = ""

    for original_url in urls:
        file = url.replace("http://clioimg.hi.u-tokyo.ac.jp/IMG", "../../docs/files/original")
        img = Image.open(file)
        thumbnail_url = original_url

        rows_1.append([id, thumbnail_url])

        rows_2.append([id, original_url, thumbnail_url, img.width, img.height])

        if thumbnail_url_0 == "":
            thumbnail_url_0 = thumbnail_url

    manifest = prefix_url + "/iiif/"+id+"/manifest.json"

    rows_0.append([id, id, thumbnail_url_0, manifest, "http://iiif.io/api/presentation/2#rightToLeftDirection", "http://universalviewer.io/examples/uv/uv.html#?manifest="+manifest, "", "https://www.hi.u-tokyo.ac.jp/tosho/shiryoriyo.html", "東京大学史料編纂所"])


df_0 = pd.DataFrame(rows_0)
df_1 = pd.DataFrame(rows_1)

with pd.ExcelWriter('data/main.xlsx') as writer:
    df_0.to_excel(writer, sheet_name='item', index=False, header=False)
    df_1.to_excel(writer, sheet_name='thumbnail', index=False, header=False)
    pd.DataFrame(rows_2).to_excel(writer, sheet_name='media', index=False, header=False)
    pd.DataFrame(rows_3).to_excel(writer, sheet_name='collection', index=False, header=False)
    pd.DataFrame([]).to_excel(writer, sheet_name='toc', index=False, header=False)



