from rdflib import Graph
import os
import xml.etree.ElementTree as ET
import urllib.parse


# os.listdir('パス')
# 指定したパス内の全てのファイルとディレクトリを要素とするリストを返す
dirname = '../docs/xml_edited'
files = os.listdir(dirname)

g = Graph()

opath = "data/iriki.rdf"

for file in files:
    if file.find(".DS") > -1:
        continue

    prefix = ".//{http://www.tei-c.org/ns/1.0}"

    print(dirname+"/"+file)

    tree = ET.parse(dirname+"/"+file)
    root = tree.getroot()
    ps = root.find(prefix+"front").findall(prefix+"persName")
    for p in list(ps):
        uri = p.get("ref")

        label = uri.split("/resource/")[1]

        label = urllib.parse.quote(label)

        rdf = "http://ja.dbpedia.org/data/"+label+".rdf"

        g.parse(rdf)

        try:

            g.parse(rdf)
        except:
            print("error:\t"+uri)

print(g.serialize(destination=opath))
