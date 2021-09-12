import json
import glob
import os
import json
from bs4 import BeautifulSoup
import datetime

today = datetime.datetime.now()

#######################


path = "data/wiki.json"

with open(path) as f:
 wiki = json.load(f)


#######################



people = {}

#######################

files = glob.glob("../../docs/file/dd/*.xml")
files = sorted(files)

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
    notes = soup.find("notesStmt").find_all("note")
    for note in notes:
        field = note.get("type")
        if field:
            item[field] = [note.text]

    #### corresp
    actions = soup.find_all("correspAction")
    for action in actions:
        field = action.get("type")
        value = action.text
        item[field] = [value.strip()]

    ### body
    body = soup.find("body")

    item["xml"] = [str(body)]

    ### date
    '''
    dates = body.find_all("date")
    date_values = []
    for date in dates:
        when = date.get("when")
        if when:
            date_values.append(when)
    
    if len(date_values) > 0:
        item["date"] = date_values
    '''

    ### entities
    entities = [
        {
            "tag": "persName",
            "label": "agential"
        },
        {
            "tag": "placeName",
            "label": "agential"
        }
    ]

    date = item["date"] if "date" in item else None

    for entity in entities:
        tags = body.find_all(entity["tag"])
        # values = []
        for tag in tags:
            corresp = tag.get("corresp")
            if corresp:
                value = corresp.replace("#", "")
                # if value not in values:
                #     values.append(value)

                if value not in people:
                    people[value] = []

                p = {
                    "name": tag.text,
                    "objectID": id,
                    "label" : item["label"]
                }

                if date:
                    p["date"] = date[0]

                people[value].append(p)

#######################  

index = []

for id in people:
    item = {
        "objectID": id,
        "label" : id,
        "list": people[id],
        "_updated": format(today, '%Y-%m-%d'),
    }

    if id in wiki:
        w = wiki[id]
        for key in w:
            item[key] = w[key]

    fw = open("/Users/nakamurasatoru/git/d_hi_tei/engishiki/static/data/people/"+id+".json", 'w')
    json.dump(item, fw, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))

    index.append(item)

#######################

# fw = open("data/index.json", 'w')
fw = open("/Users/nakamurasatoru/git/d_hi_tei/engishiki/static/data/people.json", 'w')
json.dump(index, fw, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))