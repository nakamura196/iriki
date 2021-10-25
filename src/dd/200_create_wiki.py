import json
import glob
import os
import json
from bs4 import BeautifulSoup
import datetime
import requests
today = datetime.datetime.now()
import urllib

#######################

index = []

#######################

files = glob.glob("../../docs/file/dd/*.xml")
files = sorted(files)

wiki = {}

for i in range(len(files)):

    file = files[i]

    filename = file.split("/")[-1].split(".")[0]
    
    if i % 300 == 0:
        print(str(i+1)+"/"+str(len(files))+"\t"+file)

    soup = BeautifulSoup(open(file,'r'), "xml")

    id = filename

    item = {
        "objectID": id,
        "label": soup.find("title").text,
        "_updated": format(today, '%Y-%m-%d'),
    }

    #### note
    notesStmt = soup.find("notesStmt")
    if notesStmt:
        notes = notesStmt.find_all("note")
        for note in notes:
            field = note.get("type")
            if field:
                item[field] = [note.text]
    else:
        pass
        # print("no notesStmt", id)

    #### corresp
    actions = soup.find_all("correspAction")
    for action in actions:
        field = action.get("type")
        value = action.find("persName").text
        item[field] = [value.strip()]

    ### body
    body = soup.find("body")

    item["xml"] = [str(body)]
    item["text"] = [body.text]

    ### image
    item["thumbnail"] = soup.find("graphic")["url"]
    item["manifest"] = soup.find("surfaceGrp").get("facs")

    ### date
    dates = body.find_all("date")
    date_values = []
    for date in dates:
        when = date.get("when")
        if when:
            date_values.append(when)
    if len(date_values) > 0:
        item["date"] = date_values

    ### entities
    entities = [
        {
            "tag": "persName",
            "label": "agential"
        },
        {
            "tag": "placeName",
            "label": "spatial"
        },
        {
            "tag": "name",
            "label": "about"
        }
    ]

    for entity in entities:
        tags = body.find_all(entity["tag"])
        values = []
        for tag in tags:
            corresp = tag.get("corresp")
            if corresp:
                value = corresp.replace("#", "")
                if value not in values:
                    values.append(value)

            ref = tag.get("ref")
            if ref:
                print(id, tag.text, ref)

                ref = urllib.parse.unquote(ref)

                ln = ref.split("/")[-1]

                if value in wiki:
                    continue

                w = {
                    "url": ref
                }
                wiki[value] = w

                json_url = "http://ja.dbpedia.org/data/"+ln+".json"

                df = requests.get(json_url).json()             

                if "http://ja.dbpedia.org/resource/" + ln in df:
                    df = df["http://ja.dbpedia.org/resource/" + ln]
                    if "http://ja.dbpedia.org/property/画像" in df:
                        ln2 = df["http://ja.dbpedia.org/property/画像"][0]["value"]

                        commons_url = "https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url&titles=File:" + ln2
                        df_commons = requests.get(commons_url).json()

                        pages = df_commons["query"]["pages"]
                        key = list(pages.keys())[0]
                        image_url = pages[key]["imageinfo"][0]["url"]

                        w["image"] = image_url

                    if "http://www.w3.org/2000/01/rdf-schema#comment" in df:
                        description = df["http://www.w3.org/2000/01/rdf-schema#comment"][0]["value"]
                        w["description"] = description


fw = open("data/wiki.json", 'w')
json.dump(wiki, fw, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))
