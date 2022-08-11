import requests
from bs4 import BeautifulSoup

def extract(page):
#    headers = {'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    headers = {'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    url = f'https://ua.indeed.com/jobs?q=python+developer&l=Kyiv&start={page}'
    r = requests.get(url, headers)
    return r.status_code

print(extract(0))