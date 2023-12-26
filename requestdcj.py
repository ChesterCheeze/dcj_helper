import requests
import json
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
        data = response.json()
        return data
    except:
        return None

def get_list_of_issues():
    try:
        url = f"https://he01.tci-thaijo.org/index.php/DCJ/api/v1/issues?apiToken={API_KEY}"
        response = requests.request("GET", url, headers=headers)
        data = response.json()
        return data
    except:
        return None

def get_issue_by_id(id):
    try:
        url = f"https://he01.tci-thaijo.org/index.php/DCJ/api/v1/issues/{id}?apiToken={API_KEY}"
        response = requests.request("GET", url, headers=headers)
        data = response.json()
        return data
    except:
        return None
    
def get_abstract(url):
    url_patch = f'?apiToken={API_KEY}'
    try:
        response = requests.request("GET", url+url_patch, headers=headers)
        data = response.json()
        text = data['abstract']['en_US']
        text_without_html = BeautifulSoup(text, 'html.parser').get_text()
        return text_without_html
    except:
        return None