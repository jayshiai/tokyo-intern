

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
from difflib import SequenceMatcher


#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# To interact with the client server, the headers needs to be defined
# Need to change this from the original code - Abhishek
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124'}

def similar(a, b):
    a = urlparse(a).netloc
    b = urlparse(b).netloc
    return SequenceMatcher(None, a, b).ratio()



def scrape_url(url):
    # Send a GET request to the URL
    response = requests.get(url, timeout=10, headers=headers)
    urls_1st_layer = []
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all the links from the page
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            # Make sure to handle relative URLs
            absolute_url = urljoin(url, href)
            #print(absolute_url)
            urls_1st_layer.append(absolute_url)

        # Extract text content from the page
        #text_content = soup.get_text()
        urls_1st_layer.append(url)
        urls_1st_layer = [i for i in urls_1st_layer if i.startswith('http')]
        urls_1st_layer = list(set(urls_1st_layer))
        urls_1st_layer = [scraped_url for scraped_url in urls_1st_layer if similar(url, scraped_url) > 0.75]
        
        return urls_1st_layer#, text_content

    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)
        return response.status_code

# Example usage
#url_to_scrape = "http://www.ncschina.com/"
#scraped_urls = scrape_url(url_to_scrape)
#scraped_urls

#%%

import pandas as pd
from tqdm import tqdm

#Need to change this based on the location and name of input file - Abhishek
data = pd.read_csv(r'india_new_patent_website.csv',encoding='utf-8')



chunk = data[['bvdid', 'website']]
chunk = chunk.dropna()
website_list = list(chunk.website)
bvdids = list(chunk.bvdid)
i_list = list(range(len(website_list)))
#i_ist = list(range(3))
bvdids_all = []
scraped_urls_all = []
status=[]
for i in tqdm(i_list):
    bvdid = bvdids[i]
    try:
        web_url = 'http://' + website_list[i]
        scraped_urls = scrape_url(web_url)
        if type(scraped_urls) is list:
            bvdids_all.append(bvdid)
            scraped_urls_all.append(scraped_urls)
            status.append(['Success'])
        else: #Obtaining the reason why the link was inaccessible
            bvdids_all.append(bvdid)
            scraped_urls_all.append(["N/A"])
            status.append(scraped_urls)
    except:
        try:
            web_url = 'https://' + website_list[i]
            scraped_urls = scrape_url(web_url)
            if type(scraped_urls) is list:
                bvdids_all.append(bvdid)
                scraped_urls_all.append(scraped_urls)
                status.append(['Success'])
            else: #Obtaining the reason why the link was inaccessible
                bvdids_all.append(bvdid)
                scraped_urls_all.append(["N/A"])
                status.append(scraped_urls)
        except:
            pass
bvdids_all1 = [[i] * len(j) for i, j in zip(bvdids_all, scraped_urls_all)]
bvdids_all2 = [item for items in bvdids_all1 for item in items]
status_1 = [i * len(j) for i, j in zip(status, scraped_urls_all)]
status_2 = []
for items in status_1:
    if  isinstance(items,list):
        for item in items:
            status_2.append(item)
    else:
        status_2.append(items)
        #status_2 = [item if isinstance(items,list) else items for items in status_1 for item in items]
    scraped_urls_all1 = [item for items in scraped_urls_all for item in items]
web_scraped_remain = pd.DataFrame({
                'bvdid': bvdids_all2,
                'urls': scraped_urls_all1,
                'status': status_2
                })

       
#web_scraped_remain.to_csv('G:\MS IDRP IIT Madras\Motohashi\Web Scraping\Input Files\Round 2\web_scraped_remain.csv', sep=';', index=False)
''' #You can name this file whatever you want, along with the file location. Keep the {files} - Abhishek'''
web_scraped_remain.to_excel(f'G:\MS IDRP IIT Madras\Motohashi\Web Scraping\Output Files\Round 2\web_scraped_urls_output_{files}.xlsx', index=False)
#%%
'''bvdids_all1 = [[i] * len(j) for i, j in zip(bvdids_all, scraped_urls_all)]
bvdids_all2 = [item for items in bvdids_all1 for item in items]
status_1 = [i * len(j) for i, j in zip(status, scraped_urls_all)]
status_2 = []
for items in status_1:
    if  isinstance(items,list):
        for item in items:
            status_2.append(item)
    else:
        status_2.append(items)
#status_2 = [item if isinstance(items,list) else items for items in status_1 for item in items]
scraped_urls_all1 = [item for items in scraped_urls_all for item in items]

web_scraped_remain = pd.DataFrame({
        'bvdid': bvdids_all2,
        'urls': scraped_urls_all1,
        'status': status_2
        })

#You can name this file whatever you want, along with the file location - Abhishek
#web_scraped_remain.to_csv('G:\MS IDRP IIT Madras\Motohashi\Web Scraping\Input Files\Round 2\web_scraped_remain.csv', sep=';', index=False)
web_scraped_remain.to_excel('G:\MS IDRP IIT Madras\Motohashi\Web Scraping\Input Files\Round 2\web_scraped_urls_output.xlsx', index=False)'''


