import xml.etree.ElementTree as ET
import re
import json


with open("issue_list.json") as f:
    data = json.load(f)
ISSUE_LIST = data["items"]

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

def fix_xml(xml_data: str, file_name, data_fix):

    # Parse the XML file
    # tree = ET.parse('./uploads/pubmed-20230830-153649-issues-476.xml')

    # Get the root element
    root = ET.fromstring(xml_data)

    # Modify the header element
    # volume = root.find('Article/Journal/Volume')

    # issue = root.find('Article/Journal/Issue')

    data = data_fix
    #with open("data_fix.json", "r") as f:
    #    data = json.load(f)

    # publisher.text = 'Division of Innovation and Research, Department of Disease Control, Ministry of Public Health, Thailand'

    for publisher in root.findall('Article/Journal/PublisherName'):
        publisher.text = 'Division of Innovation and Research, Department of Disease Control, Ministry of Public Health, Thailand'

    # Find all Journal elements
    # articles = root.findall('Article')


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

    # Write the modified XML to a new file
    tree = ET.ElementTree(root)
    tree.write('modified_file.xml', encoding='utf-8', xml_declaration=False)

    with open('modified_file.xml', 'r', encoding='utf-8') as f:
        contents = f.read()

    # h = '<!DOCTYPE ArticleSet PUBLIC "-//NLM//DTD PubMed 2.8//EN" "https://dtd.nlm.nih.gov/ncbi/pubmed/in/PubMed.dtd">\n' + contents
    h = '<?xml version="1.0"?>\n<!DOCTYPE ArticleSet PUBLIC "-//NLM//DTD PubMed 2.0//EN" "http://www.ncbi.nlm.nih.gov/entrez/query/static/PubMed.dtd">\n' + contents

    with open(f'{file_name} modified_file.xml', 'w', encoding='utf-8') as f:
        f.write(h)

    return f"{file_name} modified_file.xml"

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
