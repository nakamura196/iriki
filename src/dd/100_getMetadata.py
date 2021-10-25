import json
import glob
import os
import json
from bs4 import BeautifulSoup
import datetime
import pandas as pd

######

path = "../../docs/data/toc.json"

with open(path) as f:
 toc = json.load(f)

metadata2 = {}
for collection in toc:
    for item in collection["toc"]:
        id = item["url"].split("/xml/")[1].split(".")[0]

        obj = {
            "collection": collection["title"],
        }

        if "gedai" in collection:
            obj["外題"] = collection["gedai"]
        metadata2[id] = obj


######

df = pd.read_csv('data/metadata.csv', header=0)

metadata = {}

fields = {
    "タイプ" : "type",
    "received" : "received",
    "sent" : "sent",
    "date": "date"
}

for index, row in df.iterrows():
    print(index)
    # print(row)

    id = df.iloc[index]['id']

    item = {}

    if id in metadata2:
        obj = metadata2[id]
        for key in obj:
            item[key] = [obj[key]]

    metadata[id] = item

    for field in fields:

        values = df.iloc[index][field]
        if not pd.isnull(values):
            values = values.replace("？", "").replace("｜", "|")
            values = values.split("|")
            item[fields[field]] = values

fw = open("data/metadata.json", 'w')
json.dump(metadata, fw, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))