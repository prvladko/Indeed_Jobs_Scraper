# import os
from asyncore import compact_traceback
from msilib import add_stream
from xml.dom.pulldom import SAX2DOM
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

    # Outer Most Entry Point of HTML:
    outer_most_point=soup.find('div',attrs={'id': 'mosaic-provider-jobcards'})
 #       print(outer_most_point) # "UL" lists where the data are stored:

    # "UL" lists where the data are stored:
    for i in outer_most_point.find('ul'):
#        print(i.find('li'))

        # Job Title:

        job_title=i.find('h2',{'class':'jobTitle jobTitle-color-purple jobTitle-newJob'})
        print(job_title)
        if job_title != None:
 #           print(job_title)
 #           print(job_title.find('a').text)
            jobs=job_title.find('a').text

        # Company Name:

        if i.find('span',{'class':'companyName'}) != None:
            company = i.find('span',{'class':'companyName'}).text

        # Links:

        if i.find('a') != None:
            print(i.find('a'))
            print(i.find('a',{'class':'jcs-JobTitle'})['href'])
            links = i.find('a',{'class':'jcs-JobTitle'})['href']

        # Salary if available:

        if i.find('div',{'class':'attribute_snippet'}) != None:
            salary = i.find('div',{'class':'attribute_snippet'}).text
        else:
            salary='No Salary'

        # Job Post Date:

        if i.find('span', attrs={'class': 'date'}) != None:
            post_date = i.find('span', attrs={'class': 'date'}).text







indeed_dict_list=defaultdict(list)

indeed_spec=['Company', 'job', 'link', 'Salary', 'Job_Posted_date']