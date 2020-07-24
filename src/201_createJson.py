import csv
import unicodedata
import json

result = []
with open('data/html_contents_list.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    obj = {}

    for row in reader:

        text = unicodedata.normalize("NFKC", row[0])
        url = row[1]

        if text.find("外題") > -1:
            obj["gedai"] = text.replace("(外題)", "")
        elif text.find("(内容)") > -1:
            continue
        elif url != "":
            tmp = {}
            obj["toc"].append(tmp)
            tmp["title"] = text
            url = url.replace("http://www.hi.u-tokyo.ac.jp/IRIKI/JTXT/jpn_text", "")
            url = url.replace(".html", "")
            tmp["url"] = "https://tei-eaj.github.io/aozora_tei/tools/visualization/facs/?url=https://nakamura196.github.io/iriki/xml/" + url + ".xml&textDirection=vertical"
            tmp["highlight"] = False
        else:
            obj = {}
            result.append(obj)
            obj["title"] = text
            obj["toc"] = []

fw = open("../docs/data/toc.json", 'w')
json.dump(result, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
