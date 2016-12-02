import json
from bs4 import BeautifulSoup


def sort_dic_json(data):
    dic_json = {}
    for datum in data:
        for js in datum:
            if not dic_json.get(js['label'], None):
                dic_json[js['label']] = []
            dic_json[js['label']].append(js['original'].strip())
    return dic_json


with open('file.xml', 'r') as f:
    xml_data = f.read()

with open('file.json', 'r') as f:
    json_data = json.loads(f.read())

dic_json = sort_dic_json(json_data)


soup = BeautifulSoup(xml_data, 'html.parser')
lst_tag = []
lst_tag = list(set([tag.name for tag in soup.find_all()]))

correct = incorrect = 0
for tag in lst_tag:
    for text in soup.find_all(tag):
        if dic_json.get(tag, None) and text.get_text().strip() in dic_json[tag]:
            correct = correct + 1
        else:
            incorrect = incorrect + 1
print('Correct count is ', correct, ' and incorrect count is ', incorrect)

new_correct = 0
new_incorrect = 0
for tag in dic_json:
    for item in dic_json[tag]:
        if soup.find_all(tag) and item.strip() in [i.get_text().strip() for i in soup.find_all(tag)]:
            new_correct = new_correct + 1
        else:
            new_incorrect = new_incorrect + 1

print('New Correct count is ', new_correct,
      ' and New incorrect count is ', new_incorrect)
