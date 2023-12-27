import xml.etree.ElementTree as ET
import re
import json

def read_vol_issue(xml_data: str):
    tree_root = ET.fromstring(xml_data)
    volume = tree_root.find('Article/Journal/Volume')
    issue = tree_root.find('Article/Journal/Issue')
    return {'volume': volume.text, 'issue': issue.text}

def fix_xml():

    # Parse the XML file
    tree = ET.parse('./uploads/pubmed-20230830-153649-issues-476.xml')

    # Get the root element
    root = tree.getroot()

    # Modify the header element
    # volume = root.find('Article/Journal/Volume')

    # issue = root.find('Article/Journal/Issue')

    publisher = root.find('Article/Journal/PublisherName')

    with open('new_data.json') as f:
        data = json.load(f)


    # publisher.text = 'Division of Innovation and Research, Department of Disease Control, Ministry of Public Health, Thailand'

    for publisher in root.findall('Article/Journal/PublisherName'):
        publisher.text = 'Division of Innovation and Research, Department of Disease Control, Ministry of Public Health, Thailand'

    # Find all Journal elements
    articles = root.findall('Article')

    # Create a new element
    new_element = ET.Element('ArticleTitle')

    # Set the text content of the new element
    new_element.text = 'New Article Title'
    new_element.tail = '\n'

    # Insert the new element after each Journal element
    for article in articles:
        article.insert(1, new_element)


    for authorlist in root.findall('Article/AuthorList'):
        for author in authorlist.findall('Author'):
            text = author.find('Affiliation').text
            author.find('Affiliation').text = re.sub(r'\s[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)

    for journal in root.findall('Article'):
        for hist in journal.findall('History'):
            journal.remove(hist)

    for i in range(len(data['articles'])):
        for journal in root.findall('Article'):
            for title in journal.findall('ArticleTitle'):
                title.text = data['articles'][i]['title']
            for abstract in journal.findall('Abstract'):
                abstract.text = data['articles'][i]['abstract']

    for article in root.findall('Article'):
        for journal in article.findall('Journal'):
            journal.find('Issn').text = '1178-2005'

    # Write the modified XML to a new file
    tree.write('modified_file.xml', encoding='utf-8', xml_declaration=False)

    with open('modified_file.xml', 'r', encoding='utf-8') as f:
        contents = f.read()

    # h = '<!DOCTYPE ArticleSet PUBLIC "-//NLM//DTD PubMed 2.8//EN" "https://dtd.nlm.nih.gov/ncbi/pubmed/in/PubMed.dtd">\n' + contents
    h = '<?xml version="1.0"?>\n<!DOCTYPE ArticleSet PUBLIC "-//NLM//DTD PubMed 2.0//EN" "http://www.ncbi.nlm.nih.gov/entrez/query/static/PubMed.dtd">\n' + contents

    with open('modified_file_1.xml', 'w', encoding='utf-8') as f:
        f.write(h)

