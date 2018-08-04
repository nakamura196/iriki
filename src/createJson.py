import csv
import unicodedata
import json


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


result = []
with open('../data/html_contents_list.csv', 'r') as f:
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
            tmp["url"] = "mirador/?resourceUri=https://raw.githubusercontent.com/nakamura196/iriki/master/xml/" + url + ".xml&textDirection=vertical"
            tmp["highlight"] = False
        else:
            obj = {}
            result.append(obj)
            obj["title"] = text
            obj["toc"] = []

fw = open("../data/toc.json", 'w')
json.dump(result, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
