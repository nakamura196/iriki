import pandas as pd
from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from rdflib import Namespace
import numpy as np
import math
import sys
import argparse
import json
import html
import os

import requests
import shutil

def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

df = pd.read_csv("../data/images.csv", header=None, index_col=None)

r_count = len(df.index)
c_count = len(df.columns)

for j in range(1, r_count):
    url = df.iloc[j, 1]

    path = url.replace("http://clioimg.hi.u-tokyo.ac.jp/IMG", "../../docs/files/original")

    if os.path.exists(path):
        continue

    print(j, r_count)

    dirname = os.path.dirname(path)

    os.makedirs(dirname, exist_ok=True)

    download_img(url, path)