import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

def scrape_content(url):
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        text_content = soup.get_text()
        return text_content
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)
        return None

# Ensure a CSV file is provided as an argument
if len(sys.argv) != 2:
    print("Usage: python scrape.py <csv_filename>")
    sys.exit(1)

csv_filename = sys.argv[1]

# Load the CSV file
web_scraped_remain = pd.read_csv(csv_filename)
web_scraped_remain = web_scraped_remain.dropna()

urls = list(web_scraped_remain['urls'])
bvdids = list(web_scraped_remain['bvdid'])
content = []
status = []
for url in tqdm(urls, desc='Processing', unit='item'):
    try:
        text = scrape_content(url)
        if(text is not None):
            content.append(text)
            status.append('Success')
        else:
            content.append(None)
            status.append('Failed')
    except:
        content.append(None)
        status.append('Failed')

web_scraped_content = pd.DataFrame({
    'bvdid': bvdids,
    'urls': urls,
    'text': content,
    'status': status
})

output_filename = csv_filename.replace('linkList_chunk', 'web_scraped_content_chunk')
web_scraped_content.to_csv(output_filename, index=False)
