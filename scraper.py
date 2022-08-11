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

    #Connecting to "Location" Indeed
    url = 'https://indeed.co.in/jobs&q=' + skill + \
    '&l=' + place + '&sort=date' +'&start='+ str(page * 10)

    # Get request to indeed with headers above (don't need headers!)
    response = requests.get(url)
    html = response.text

    # Scrapping the Web (can use 'html' or 'lxml')
    soup = BeautifulSoup(html, 'lxml')

    # Outer Most Entry Point of HTML:
    outer_most_point=soup.find('div',attrs={'id': 'mosaic-provider-jobcards'})
 #       print(outer_most_point)

    # "UL" lists where the data are stored:
    for i in outer_most_point.find('ul'):
#        print(i.find('li'))

        # Job Title:

        job_title=i.find('h2')
#        job_title=i.find('h2',{'class':'jobTitle jobTitle-color-purple jobTitle-newJob'})
#        print(job_title)
 #       if job_title != None:
 #           print(job_title)
 #           print(job_title.find('a').text)
 #           jobs=job_title.find('a').text
        # 2022 AFTER WEBSITE CHANGES        
        if job_title != None:
    
            jobs=job_title.find('span').text
#                 print(job_titles)
# #                 print('shit')
#             else:
# #                 jobs=job_title.find('a').text
#                 print('shit')       

        # Company Name:

        if i.find('span',{'class':'companyName'}) != None:
            company = i.find('span',{'class':'companyName'}).text

        # Links: these Href links will take us to full job description

        if i.find('a') != None:
#            print(i.find('a'))
#            print(i.find('a',{'class':'jcs-JobTitle'})['href'])
            links = i.find('a',{'class':'jcs-JobTitle'})['href']

        # Salary if available:

        if i.find('div',{'class':'attribute_snippet'}) != None:
            salary = i.find('div',{'class':'attribute_snippet'}).text
        else:
            salary='No Salary'

        # Job Post Date:

        if i.find('span', attrs={'class': 'date'}) != None:
            post_date = i.find('span', attrs={'class': 'date'}).text

        # Put everything together in a list of lists for the default dictionary

        indeed_posts.append([company,jobs,links,salary,post_date])


# put together in a list


# (create a dictionary with keys and a list of values from above "indeed_posts")

indeed_dict_list=defaultdict(list)

# Fields for our DF

indeed_spec=['Company', 'job', 'link', 'Salary', 'Job_Posted_date']

print('These Href links will go to a new page containing full job description')
print('\n')
print(pd.DataFrame(indeed_posts,columns=indeed_spec)['link'][0]) 
#these are not the same, probably from recruiter(s)
print(pd.DataFrame(indeed_posts,columns=indeed_spec)['link'][1])

pd.DataFrame(indeed_posts,columns=indeed_spec)

# Get all qualification page text: key=index, value=string of text for qualification

job_descr_txt=[]

# Indeed DF with columns we made above and the stored data from scraping
Indeed_DF = pd.DataFrame(indeed_posts,columns=indeed_spec)

# convert Series to lists of strings
my_super_fun_Indeed_links = list(Indeed_DF['link'])

# iterator will be our index value for default_dict_list
for i in range(len(my_super_fun_Indeed_links)):
    
    url_href='https://in.indeed.com' + my_super_fun_Indeed_links[i]
#     print(url_href)
    response = requests.get(url_href, headers=headers)
    html_ = response.text
    soup_ = BeautifulSoup(html_, 'lxml')
    
    for ii in soup_.find('div',{'class':'jobsearch-jobDescriptionText'}):
        try:
            job_descr_txt.append([i,''.join(ii.text.strip())])
        except AttributeError:
            job_descr_txt.append([i,''])
job_descr_txt
      
# https://in.indeed.com/viewjob?cmp=Alpha-Net-Technologies-Pvt-Ltd&t=Database+Developer+Analyst&jk=a5063bed6e53cb53&vjs=3

# https://in.indeed.com/viewjob?q=/company/Alpha-Net-Technologies-Pvt-Ltd/jobs/Database-Developer-Analyst-a5063bed6e53cb53?fccid=0e8473839d79bdf1&vjs=3

# create dictionary with values as lists
dct_lst= defaultdict(list)

for i in job_descr_txt:
    #key value pairs for default_dict_list
    dct_lst[i[0]].append(i[1])
    
dict_lst_jobsDescr=[]

for i in dct_lst.values(): # string join: lists of lists of strings
    dict_lst_jobsDescr.append(''.join(i))
    
dict_lst_jobsDescr[1]

Indeed_DF['text_descrption'] = dict_lst_jobsDescr
Indeed_DF.head()