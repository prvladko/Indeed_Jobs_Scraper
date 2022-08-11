import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime, timedelta
import datetime
from pymongo import MongoClient


def INIT():
    try:
        print("INIT - Started")
        global SearchQuery
        global SearchLocation
        global startPage
        global numPages
        
        SearchQuery='data scientist $20,000'
        SearchLocation='New York'
        startPage=0
        numPages=3
    except (ValueError,IOError) as err:
        print("INIT - Error Occured \n"+str(err))    

def format_time():
    try:
        t = datetime.datetime.now()
        s = t.strftime('%m-%d-%Y %H:%M:%S.%f')
        return s[:-3]
    except (ValueError,IOError) as err:
        print("format_time - Error Occured \n"+str(err))

def request(SearchQuery,SearchLocation,Page):
    try:
        print("request - Started")
#        URL = "https://www.indeed.com/jobs?q="+str(SearchQuery)+"&l="+str(SearchLocation)+"&start="+str(Page)
        URL = 'https://indeed.co.in/jobs&q=' + str(SearchQuery) + '&l=' + str(SearchLocation) + '&sort=date' +'&start='+ str(Page * 10)       
        print("request - URL\n"+str(URL))
          
        return html_text
    except (ValueError,IOError) as err:
        print("request - Error Occured \n"+str(err))
        
def JobCardScrap(html_text,pageNum):
    try:
        print("JobCardScrap - Started")
        soup = BeautifulSoup(html_text, 'html.parser')

        print("JobCardScrap - soup Created")

        Jobs = soup.find('div', id="mosaic-zone-jobcards")
        Jobs = Jobs.find_all('a', id=re.compile("^job"))

        Jobs_List=[]
        Jobs_Dict={}

        print("JobCardScrap - Jobs Extracted")

        for job in Jobs:
            Jobs_Dict={} 
            Jobs_Dict["pageNum"]=pageNum

            Jobs_Dict["extractionDate"]=str(format_time())
            
            jobTitle=job.find('h2', class_='jobTitle')
            Jobs_Dict["jobTitle"]=jobTitle.text
            
            companyName=job.find('span', class_='companyName')
            Jobs_Dict["companyName"]=companyName.text

            
            ratingNumber=job.find('span', class_='ratingNumber')
            if ratingNumber:
                Jobs_Dict["ratingNumber"]=ratingNumber.text

            companyLocation=job.find('div', class_='companyLocation')
            Jobs_Dict["companyLocation"]=companyLocation.text


            jobsnippet=job.find('div', class_='job-snippet')
            Jobs_Dict["jobsnippet"]=jobsnippet.text

            
            date=job.find('span', class_='date')
            if date:
                Jobs_Dict["date"]=date.text

            Jobs_Dict["jobLink"]="https://www.indeed.com"+job['href']

                
            Jobs_List.append(Jobs_Dict)
    
            print("JobCardScrap - Job DICT Appended")

                
            print("JobCardScrap - Data\n"+str(Jobs_Dict))
            
        return Jobs_List
    except (ValueError,IOError) as err:
        print("JobCardScrap - Error Occured \n"+str(err))    

def MongoConnect():
    try:
        print("MongoConnect - Started")
        CONFIGS = {
            "DB_Username" : "admin",
            "DB_Password" : "admin",
            "authSource" : "test",
            "DB_IP" : "192.168.182.140",
            "DB_PORT" : 27017
        }
        print("MongoConnect() - Started","n")
        print("MongoConnect() - Setting Connection String","n")
        myclient = MongoClient(
            host=CONFIGS["DB_IP"], 
            port=CONFIGS["DB_PORT"], 
            username=CONFIGS["DB_Username"],
            password=CONFIGS["DB_Password"],
            authSource=CONFIGS["authSource"]
            )
        print("MongoConnect() - Returning Connection Client","n")
        return myclient
    except (ValueError,IOError) as err:
        print("MongoConnect - Error Occured \n"+str(err)) 

def mongo_add(mongoClient,db,col,payload):
    try:
        print("mongo_add - Started")
        mydb = mongoClient[db]
        mycol = mydb[col]
        if isinstance(payload, dict):
            mycol.insert(payload)
            return str(payload)
        elif isinstance(payload, list):
            mycol.insert_many(payload)
            return str(payload)
    except (ValueError,IOError) as err:
        print("mongo_add - Error Occured \n"+str(err))

def MAIN():
    try:
        print("Main - Started")
        INIT()
        allJobs_List=[]
        
        mongoClient=MongoConnect()
        
        for i in range(numPages):
            Page=i*10
            html_text=request(SearchQuery,SearchLocation,Page)
            Jobs_List=JobCardScrap(html_text,i+1)
            
            mongo_add(mongoClient,"Indeed","Jobs_1",Jobs_List)
            
            allJobs_List.extend(Jobs_List)
        df=pd.DataFrame(allJobs_List)
        print(df)
    except (ValueError,IOError) as err:
        print("Main - Error Occured \n"+str(err))
        
MAIN()