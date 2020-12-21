import requests
from bs4 import BeautifulSoup
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import csv
#let us do webscrapping using selenium
#instead of giving inputs let us extract inputs from the site
#based on that let us do web scrapping for top 3 pages
def SCROLL_TO_BOTTOM(browser):
    html = browser.find_element_by_tag_name('html')
    html.send_keys(Keys.END)
def main(job,location):
    browser = webdriver.Chrome('C:\\Users\\Taha\\Desktop\\chromedriver.exe')
    browser.get('https://www.linkedin.com/jobs/')
    time.sleep(10)
    path='https://www.linkedin.com/jobs/'
    jobtitle=browser.find_element_by_name("keywords")
    jobtitle.send_keys(job)
    location1=browser.find_element_by_name("location")
    location1.send_keys(location)
    button=browser.find_element_by_xpath("""/html/body/main/section[1]/section/div[2]/button[2]""")
    button.click()
    #jobpath=path+'search?keywords='+job+'&location='+location+'=&redirect=false&position=1&pageNum=0'
    #browser.get(jobpath)
    time.sleep(2)
    #now scrap the data from the site
    details=set()
    i=0
    while(i<1):
        r=browser.find_element_by_xpath("""//*[@id="main-content"]/div/section/ul""")
        ele=r.find_elements_by_tag_name('li')
        for tag in ele:
            time.sleep(1)
            p=tag.find_elements_by_tag_name('div')
            for tag2 in p:
                details.add(tag2.text)
        SCROLL_TO_BOTTOM(browser)
        time.sleep(2)
        i=i+1
    jobdetails=list(details)
    location=[]
    postedtime=[]
    designation=[]
    company=[]
    finallist=[]
    for jobpost in jobdetails:
        sp=(jobpost.splitlines())
        if(len(sp)==4):
            list_temp=[sp[0],sp[1],sp[2],sp[3]]
            finallist.append(list_temp)
    columns=['Company','Designation','Location','PostedTime']
    df=pd.DataFrame(finallist)
    df.columns=columns
    df.to_csv('output_linkedIn_jobs.csv')

    print('CSV DOWNLOADED !')
if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])
