import json
import re
from requestdcj import get_abstract, get_current_issue


data = get_current_issue()

new_data = {}

new_data['articles'] = []

for article in data['articles']:
    text = article['publications'][0]['fullTitle']['en_US']
    text_without_xs = re.sub(' +', ' ', ' '.join(text.split()))
    url = article['publications'][0]['_href']
    abstract = get_abstract(url)
    new_data['articles'].append({'title': text_without_xs, 'abstract': abstract})


with open('new_data.json', 'w', encodeing='utf-8') as f:
    json.dump(new_data, f, indent=4, ensure_ascii=False)



