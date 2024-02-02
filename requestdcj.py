import requests
import json
import re
from bs4 import BeautifulSoup
    
with open("api_key.json") as f:
    data = json.load(f)

API_KEY = data["api_key"]

headers = {
    'User-Agent': 'DCJ App v1.0'
}

def get_current_issue():
    try:
        url = f"https://he01.tci-thaijo.org/index.php/DCJ/api/v1/issues/current?apiToken={API_KEY}"
        response = requests.request("GET", url, headers=headers)
        return response.json()
    except:
        return None

def get_list_of_issues():
    try:
        url = f"https://he01.tci-thaijo.org/index.php/DCJ/api/v1/issues?apiToken={API_KEY}"
        response = requests.request("GET", url, headers=headers)
        return response.json()
    except:
        return None

def get_issue_by_id(id: str):
    try:
        url = f"https://he01.tci-thaijo.org/index.php/DCJ/api/v1/issues/{id}?apiToken={API_KEY}"
        response = requests.request("GET", url, headers=headers)
        return response.json()
    except:
        return None

def get_tag(soup):
    myset = set()
    for tag in soup():
        if tag.name not in ['sup', 'sub', 'b', 'i', 'u']:
            myset.add(tag.name)
    
    return myset

def create_replacements(set_of_tags):
    replacements = {}
    for tag in set_of_tags:
        if tag == 'em':
            replacements[f'<{tag}>'] = '<i>'
            replacements[f'</{tag}>'] = '</i>'
        else:
            replacements[f'<{tag}>'] = ''
            replacements[f'</{tag}>'] = ''
        
    return replacements

def clean_text(text, replacements):
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)

    return text

def get_abstract(url):
    url_patch = f'?apiToken={API_KEY}'
    try:
        response = requests.request("GET", url+url_patch, headers=headers)
        data = response.json()
        text = data['abstract']['en_US']
        soup = BeautifulSoup(text, 'html.parser')
        tag_set = get_tag(soup)
        replacements = create_replacements(tag_set)
        return clean_text(text, replacements)
    except:
        return None
    
raw_text = "<p>This &#x078;&#x304; predictive research aimed to study the level of health literacy in stroke prevention among elderly people with hypertension and examine the factors affecting knowledge on health literacy in stroke prevention among elderly with hypertension in Nakhon Sawan Province. A total of 410 samples aged over 60 years with high blood pressure who had lived in Nakhon Sawan Province were recruited by systematic sampling. The data were collected between February-March 2021. The tool was a questionnaire with the Cronbach's alpha between 0.84-0.94. The data were analyzed by frequency distribution, percentage, mean, standard deviation, and stepwise multiple linear regression at a level of statistical significance of 0.05. The results revealed that the samples had health literacy in stroke prevention at a fair level ( <em>=</em>76.57, SD=14.11) and the statistically significance predictive factors of health literacy in stroke prevention among elderly people with hypertension in Nakhon Sawan Province included living in an urban area <em>(</em><em>p</em><em>-value&lt;0.001, R<sup>2</sup>=0.102, </em><em>β</em><em>=0.273)</em>, self-awareness <em>(</em><em>p</em><em>-value&lt;0.001, R<sup>2</sup>=0.062, </em><em>β</em><em>=0.213), </em>level of ability to carry out daily activities <em>(</em><em>p</em><em>-value&lt;0.001, R<sup>2</sup>=0.057, </em><em>β</em><em>=0.189)</em>, education level at least Secondary school <em>(</em><em>p</em><em>-value&lt;0.001, R<sup>2</sup>=0.035, </em><em>β</em><em>=0.150)</em>, body mass index <em>(</em><em>p</em><em>-value=0.005, R<sup>2</sup>=0.018, </em><em>β</em><em>=0.124)</em>, obtaining more than one source of information <em>(</em><em>p</em><em>-value=0.007, R<sup>2</sup>=0.017, </em><em>β</em><em>=0.115)</em>, and age <em>(</em><em>p</em><em>-value=0.006, R<sup>2</sup>=0.013, </em><em>β</em><em>=-0.129)</em>. The result from this study should support for the relevant agencies in planning the stroke prevention program, such as creating appropriate media, contact channels in case of warning symptoms, for the elderly and enhancing health literacy in the elderly with high blood pressure.</p>"

soup = BeautifulSoup(raw_text, 'html.parser')

