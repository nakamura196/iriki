import json
import glob
import os
import json
from bs4 import BeautifulSoup
import datetime

today = datetime.datetime.now()

#######################

index = []

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

        if len(values) > 0:
            item[entity["label"]] = values

    ####

    fw = open("/Users/nakamurasatoru/git/d_hi_tei/engishiki/static/data/item/"+id+".json", 'w')
    json.dump(item, fw, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))

    ####

    fulltexts = []
    for key in item:
        value = item[key]
        if type(value) is not str:
            value = ", ".join(value)
        fulltexts.append(value)
    item["fulltext"] = ", ".join(fulltexts)

    index.append(item)
    

#######################

# fw = open("data/index.json", 'w')
fw = open("/Users/nakamurasatoru/git/d_hi_tei/engishiki/static/data/index.json", 'w')
json.dump(index, fw, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))

# oDir = "../../u-renja/static/data"

'''
configs = [
    {
        "id": "person",
        "tag": "persName"
    },
    {
        "id": "place",
        "tag": "placeName"
    }
]
'''

'''
map = {}

for config in configs:
    map[config["id"]] = {}

for i in range(len(files)):

    file = files[i]

    filename = file.split("/")[-1].split(".")[0]
    
    if i % 300 == 0:
        print(str(i+1)+"/"+str(len(files))+"\t"+file)

    soup = BeautifulSoup(open(file,'r'), "xml")

    ######

    body = soup.find("body")

    if not body:
        continue

    for config in configs:

        conf_id = config["id"]
        conf_tag = config["tag"]

        map4index = map[conf_id]

        tags = body.find_all(conf_tag)
        for tag in tags:
            
            name = tag.text

            id = filename + "_" + name.replace(" ", "_").replace("\t", "_t_").replace("\n", "_n_")

            if id not in map4index:
                item = {
                    "objectID": id,
                    "label": name,
                    "file": [],
                    "fulltext": name
                }

                map4index[id] = item

            item = map4index[id]
            if filename not in item["file"]:
                item["file"].append(filename)

for config in configs:
    conf_id = config["id"]
    map4index = map[conf_id]
    index = []
    for id in map4index:

        item = map4index[id]

        item_path = oDir + "/item/" + id + ".json"

        os.makedirs(os.path.dirname(item_path), exist_ok=True)

        fw = open(item_path, 'w')
        json.dump(item, fw, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))

        index.append(
            item
        )

    fw = open(oDir + "/" +conf_id+ ".json", 'w')
    json.dump(index, fw, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))
'''

