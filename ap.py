import argparse
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


def get_lst_tag(soup):
    return list(set([tag.name for tag in soup.find_all()]))


def execute_code(xml_file, json_file):
    with open(xml_file, 'r') as f:
        xml_data = f.read()

    with open(json_file, 'r') as f:
        json_data = json.loads(f.read())
    soup = BeautifulSoup(xml_data, 'html.parser')
    lst_tag = get_lst_tag(soup)

    lst = []
    for index, data in enumerate(json_data):
        count_find = 0
        count_not_find = 0
        for item in data:
            if (search_in_xml_specific_tag(soup, item['label'], item['original'])):
                count_find = count_find + 1
            else:
                count_not_find = count_not_find + 1

        lst.append((count_find, count_not_find))
    print(lst)

    # dic_json = sort_dic_json(json_data)

    # correct, incorrect = 0, 0
    # for tag in lst_tag:
    #     for text in soup.find_all(tag):
    #         if dic_json.get(tag, None) and text.get_text().strip() in dic_json[tag]:
    #             correct = correct + 1
    #         else:
    #             incorrect = incorrect + 1
    # print('Correct count is ', correct, ' and incorrect count is ', incorrect)


def search_in_xml_specific_tag(soup, tag, item):
    if soup.find_all(tag) and item.strip() in [i.get_text().strip() for i in soup.find_all(tag)]:
        return True
    else:
        return False


# def search_in_xml_not_specific_tag(soup, tag, item, lst_tag):
#     lst_tag = lst_tag - tag
#     for i in


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('xml_file', help='xml file')
    parser.add_argument('json_file', help='json file')
    args = parser.parse_args()
    execute_code(args.xml_file, args.json_file)


if __name__ == '__main__':
    main()


def plot_graph(TP, FP, TN, FN):
    '''
    TP = correct
    FP = incorrect
    TN = new_correct
    FN = new_incorrect
    '''
    import matplotlib.pyplot as plt
    import numpy as np
    x = FP / (FP + TN)
    y = TP / (TP + FN)

    # This is the ROC curve
    plt.plot(x, y)
    plt.show()

    # This is the AUC
    auc = np.trapz(y, x)
