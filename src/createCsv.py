# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
import os
from xml.dom.minidom import parseString
import unicodedata
import xml.etree.ElementTree as ET
import csv


def get_images(image_url):

    image_urls = []

    html = requests.get(image_url)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html.content, "html.parser")
    links = soup.find_all("a")

    for link in links:
        image_urls.append(link.get("href"))
    return image_urls


def get_header_links(soup_):
    image_urls_ = []
    translation_urls_ = []

    links = soup_.find_all("a")

    for link in links:
        text = link.string
        if text is None:
            continue
        if text == "画　像":
            image_url = link.get("href")

            image_url = image_url.replace("'", "\"")
            image_url = image_url.split("\"")[1]

            if image_url.find(".jpg") > -1:
                image_urls_.append(image_url)
            elif image_url.find(".html") > -1:
                image_url = image_url.replace("..", "http://www.hi.u-tokyo.ac.jp/IRIKI")
                image_url = image_url.replace("/img", "/imgix")
                image_urls_ = get_images(image_url)
        elif text.find("英文-#") != -1:
            translation_url = link.get("href")
            translation_url = translation_url.replace("..", "http://www.hi.u-tokyo.ac.jp/IRIKI")
            translation_urls_.append(translation_url)

    return image_urls_, translation_urls_


def modi(text):
    text = str(text)
    text = text.split("</a>）<br>")[1]
    text = text.split("\n</br></br>")[0]
    text = text.strip()

    text = "<lb/>" + text.replace("<br>", "<lb/>")

    return text


def rep(text, comments):

    text = text.replace("false", "true")
    text = text.replace('<a href="#0" onmouseout="StartShow(', "")
    text = text.replace('true)" onmouseover="StartShow(', "")
    text = text.replace(',true)">', "")
    text = text.replace('</a>', "</span>")

    for i in range(len(comments)):
        num = str(i)
        text = text.replace(num + "," + num, '<span corresp="#' + comments[i] + '">')

    return text


def get_text_contents(soup_):
    text_body = soup_.find("hr")
    try:

        text_body = modi(text_body)

        script_text = soup_.find("script")
        script_text = script_text.string.split("var comments = new Array();")[1]
        comments_str = script_text.split("'")
        comments = []
        for i in range(1, len(comments_str), 2):
            comment = unicodedata.normalize("NFKC", comments_str[i]).replace("(", ")").replace(")", "")
            comments.append(comment)
        # print(comments)

        text_body = rep(text_body, comments)

        return text_body, comments
    except:
        return None, None


def create_xml(title, text, comments, image_urls, oid):
    xml_template = '<?xml version="1.0" encoding="UTF-8"?>\
<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>\
<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml"\
	schematypens="http://purl.oclc.org/dsdl/schematron"?>\
<TEI xmlns="http://www.tei-c.org/ns/1.0">\
   <teiHeader>\
      <fileDesc>\
         <titleStmt>\
            <title></title>\
         </titleStmt>\
         <publicationStmt>\
            <p>Publication Information</p>\
         </publicationStmt>\
         <sourceDesc>\
            <p>Information about the source</p>\
         </sourceDesc>\
      </fileDesc>\
   </teiHeader>\
   <facsimile>\
      <surfaceGrp>\
      </surfaceGrp>\
   </facsimile>\
   <text>\
      <front>\
         <p>\
         </p>\
      </front>\
      <body><p>' + text + '</p></body>\
   </text>\
</TEI>'

    try:
        dom = parseString(xml_template)

        titleNode = dom.getElementsByTagName("title")[0]
        titleNode.appendChild(dom.createTextNode(title))

        front_p = dom.getElementsByTagName("front")[0].getElementsByTagName("p")[0]

        for comment in set(comments):
            span = dom.createElement('span')
            span_attr = dom.createAttribute('xml:id')
            span_attr.value = comment
            span.setAttributeNode(span_attr)
            front_p.appendChild(span)

            span2 = dom.createElement('span')
            span.appendChild(span2)
            span2.appendChild(dom.createTextNode(comment))

        surfaceGrp = dom.getElementsByTagName("surfaceGrp")[0]

        for image_url in image_urls:
            surface = dom.createElement('surface')
            surfaceGrp.appendChild(surface)

            graphic = dom.createElement('graphic')
            surface.appendChild(graphic)

            g_attr = dom.createAttribute('url')
            g_attr.value = image_url
            graphic.setAttributeNode(g_attr)

        # domをxmlに変換して整形
        return str(dom.toprettyxml())
    except:
        print(title)
        return None


# os.listdir('パス')
# 指定したパス内の全てのファイルとディレクトリを要素とするリストを返す
dirname = '/Users/satoru/git/iriki/xml'
files = os.listdir(dirname)

fi = open('images.csv', 'w')
writer = csv.writer(fi, lineterminator='\n')
writer.writerow(["Item Identifier", "Media Url"])

for file in files:
    if file.find(".DS") > -1:
        continue

    prefix = ".//{http://www.tei-c.org/ns/1.0}"

    print(dirname+"/"+file)

    tree = ET.parse(dirname+"/"+file)
    root = tree.getroot()
    gs = root.findall(prefix+"graphic")
    for g in list(gs):
        url = g.get("url")

        writer.writerow([file.split(".")[0], url])

fi.close()

# ----

fi = open('iriki.csv', 'w')
writer = csv.writer(fi, lineterminator='\n')
writer.writerow(["dcterms:identifier", "dcterms:title"])

for file in files:
    if file.find(".DS") > -1:
        continue

    id = file.split(".")[0]

    prefix = ".//{http://www.tei-c.org/ns/1.0}"

    tree = ET.parse(dirname+"/"+file)
    root = tree.getroot()
    title = root.find(prefix+"title").text
    print(title)
    title = title + "_nakamura196maeda"

    writer.writerow([id, title])

fi.close()
