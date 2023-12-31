import json
import re
from requestdcj import get_abstract, get_issue_by_id

#iss = get_issue_by_id("17810")

async def build_data_fix(issue_data):
    
    data = issue_data

    new_data = {}

    new_data['articles'] = []

    for article in data['articles']:
        text = article['publications'][0]['fullTitle']['en_US']
        text_without_xs = re.sub(' +', ' ', ' '.join(text.split()))
        url = article['publications'][0]['_href']
        abstract = get_abstract(url)
        new_data['articles'].append({'title': text_without_xs, 'abstract': abstract})

    #with open("data_fix.json", "w") as f:
    #    json.dump(new_data, f)

    return new_data



