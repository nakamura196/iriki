# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
import urllib.request, json
from xml.dom.minidom import parseString
import unicodedata
import pandas as pd

rows = []
rows.append(["id", "url"])

with open('data/html_contents_list.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    count = 0

    for row in reader:
        if len(row) > 1 and row[1] != "":

            count += 1

            if count > 0:

                title = row[0].strip()

                id = unicodedata.normalize("NFKC", title).split("#")[1].split(")")[0]

                url = row[1]
                print("url:\t" + url)

                sleep(1)

                html = requests.get(url)

                # htmlをBeautifulSoupで扱う
                soup = BeautifulSoup(html.content, "html.parser")

                aas = soup.find_all("a")

                for aa in aas:
                    href = aa.get("href")

                    if href == None:
                        continue

                    if ".jpg" in href:
                        hrefs = href.split("\"")
                        for aaa in hrefs:
                            if ".jpg" in aaa:
                                
                                rows.append([id, aaa])

                    elif "IMG" in href:
                        url2 = href.split("'")[1]
                        url2 = url2.replace("../", "http://www.hi.u-tokyo.ac.jp/IRIKI/")
                        url2 = url2.replace("img", "imgix")

                        html2 = requests.get(url2)

                        # htmlをBeautifulSoupで扱う
                        soup2 = BeautifulSoup(html2.content, "html.parser")
                        
                        aas2 = soup2.find_all("a")
                        for aa2 in aas2:
                            href2 = aa2.get("href")
                            
                            rows.append([id, href2])

            if count > 10 and False:
                break



df = pd.DataFrame(rows)
df.to_csv("data/images.csv", index=False, header=False)