# import os
from msilib import add_stream
import requests
from bs4 import BeautifulSoup # webscrape
from collections import defaultdict # default dictionary: store a list with each key
import pandas as pd # DF
import re           # regular expressions
import datetime     # format date/time

# system details
headers = {'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

# Skills & Place of Work
skill = input('Enter your Skill: ').strip()
place = input('Enter the location: ').strip()
no_of_pages = int(input('Enter the # of pages to scrape: '))

indeed_posts=[]

for page in range(no_of_pages):

    url = 'https://indeed.co.in/jobs&q=' + skill + '&l=' + place + '&sort=date' +'&start='+ str(page * 10)

    response = requests.get(url, headers=headers)
    html = response.text

    # Scrapping the Web ('html' or 'lxml')
    soup = BeautifulSoup(html, 'lxml')

