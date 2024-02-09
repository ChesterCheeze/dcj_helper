import xml.etree.ElementTree as ET
import re
import json


def load_list_of_issues(file_name):
    with open(file_name) as f:
        data = json.load(f)
    return data["items"]

ISSUE_LIST = load_list_of_issues("issue_list.json")

def read_vol_issue(xml_data: str):
    tree_root = ET.fromstring(xml_data)
    volume = tree_root.find('Article/Journal/Volume')
    issue = tree_root.find('Article/Journal/Issue')
    return {'volume': int(volume.text), 'issue': str(issue.text)}

def get_issue_id(vol: int, issue: str):
    for item in ISSUE_LIST:
        if item['volume'] == vol and item['number'] == issue:
            return item['id']
    return None

def fix_title(root, data):

    data_indx = 0

    # Insert the new element after each Journal element
    for article in root.findall("Article"):
        # Create a new element
        new_element = ET.Element('ArticleTitle')
        # Set the text content of the new element
        new_element.text = data["articles"][data_indx]["title"]
        new_element.tail = '\n'
        article.insert(1, new_element)
        data_indx = data_indx + 1

def fix_xml(xml_data: str, file_name, data_fix):

    root = ET.fromstring(xml_data)
    data = data_fix

    for publisher in root.findall('Article/Journal/PublisherName'):
        publisher.text = 'Department of Disease Control, Ministry of Public Health, Thailand'

    for authorlist in root.findall('Article/AuthorList'):
        for author in authorlist.findall('Author'):
            text = author.find('Affiliation').text
            author.find('Affiliation').text = re.sub(r'\s[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)

    for journal in root.findall('Article'):
        for hist in journal.findall('History'):
            journal.remove(hist)

    fix_title(root, data)
          
    indx = 0
    for article in root.findall("Article"):
        article.find("Abstract").text = data["articles"][indx]["abstract"]
        indx = indx + 1

    for article in root.findall('Article'):
        for journal in article.findall('Journal'):
            journal.find('Issn').text = '1178-2005'

    # Get all Article elements
    articles = root.findall('Article')

    # Sort the articles by the text content of the FirstPage element
    sorted_articles = sorted(articles, key=lambda article: int(article.find('FirstPage').text))

    # Remove the original Article elements from the root
    for article in articles:
        root.remove(article)

    # Add the sorted Article elements to the root
    for article in sorted_articles:
        root.append(article)

    # Write the modified XML to a new file
    tree = ET.ElementTree(root)
    tree.write('modified_file.xml', encoding='utf-8', xml_declaration=False)

    with open('modified_file.xml', 'r', encoding='utf-8') as f:
        contents = f.read()

    h = '<!DOCTYPE ArticleSet PUBLIC "-//NLM//DTD PubMed 2.8//EN" "https://dtd.nlm.nih.gov/ncbi/pubmed/in/PubMed.dtd">\n' + contents

    with open(f'{file_name}', 'w', encoding='utf-8') as f:
        f.write(h)

    return f"{file_name}"