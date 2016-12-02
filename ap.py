import json
from bs4 import BeautifulSoup


def sortJson(data):
    jsonNewArray = {}
    for datum in data:
        for js in datum:
            if not jsonNewArray.get(js['label'], None):
                jsonNewArray[js['label']] = []
            jsonNewArray[js['label']].append(js['original'].strip())
    return jsonNewArray


with open('file.xml', 'r') as f:
    xmlData = f.read()

with open('file.json', 'r') as f:
    jsonData = json.loads(f.read())

sortedJsonData = sortJson(jsonData)


soup = BeautifulSoup(xmlData, 'html.parser')
tagsArray = []
tagsArray = list(set([tag.name for tag in soup.find_all()]))

correct = incorrect = 0
for tag in tagsArray:
    for tagText in soup.find_all(tag):
        if sortedJsonData.get(tag, None) and tagText.get_text().strip() in sortedJsonData[tag]:
            # print('Correct', tagText.get_text())
            correct = correct + 1
        else:
            # print('Not Correct', tagText.get_text())
            incorrect = incorrect + 1
print('Correct count is ', correct, ' and incorrect count is ', incorrect)
