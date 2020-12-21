import os,random,sys,time
from time import sleep
from urllib.parse import urlparse
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import pandas as pd
def main(companyname):
    driver = webdriver.Chrome('C:\\Users\\Taha\\Desktop\\chromedriver.exe')
    driver.get('https://www.google.com/')
    src= driver.find_element_by_xpath("""//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input""")
    src.send_keys('tracxn '+companyname)
    src.send_keys(Keys.ENTER)
    time.sleep(5)
    src= driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    search= soup.find('div',id='search')
    link=search.find(class_='g')
    a_tag=link.find('a', href=True)
    url=a_tag['href']
    driver.get(url)
    time.sleep(5)
    t=driver.page_source
    soup = BeautifulSoup(t,'lxml')
    time.sleep(5)
    overview_details=set()
    overview_values=[]
    date=[]
    funding_amt=[]
    funding_rnd=[]
    investor_details=[]
    investors1=[]
    location=[]
    overview=soup.findAll("p",{"class":"txn--margin-bottom-lg txn--seo-companies__overview-info txn--display-flex-row"})
    for item in overview:
        try:
            overview_details.add(item.contents[0].text)
            overview_values.append(item.contents[1].text)
        except:
            overview_details.add(item.contents[0].text)
            overview_values.append(item.contents[1])
    time.sleep(5)
    funding=soup.find_all("tr",{"class":"txn--vertical-align-top"})
    for item in funding:
        date.append(item.contents[0].text)
        funding_amt.append(item.contents[1].text)
        funding_rnd.append(item.contents[2].text)
        investor_details.append(item.contents[3].text)
    time.sleep(5)
    investors=soup.find_all("div",{"class":"txn--display-flex-column txn--flex-align-center txn--margin-horizontal-sm txn--flex-1 txn--text-caption txn--text-center"})
    for item in investors:
        try:
            investors1.append(item.contents[1].text)
            location.append(item.contents[2].text)
        except:
            investors1.append(item.contents[1].text)
            location.append(item.contents[2])
    overview_details=list(overview_details)
    # print(overview_details)
    # print(overview_values)
    # print(investor_details)
    # print(date)
    # print(funding_amt)
    # print(funding_rnd)
    # print(investor_details)
    # print(investors1)
    # print(location)
    new_loc=[]
    for loc in location:
        p=[]
        e=loc.split(',')
        for val in e:
            if ((val[0].isdigit()==False) and (val[0]!='$')):
                p.append(val)
            p1=''.join(p)
        new_loc.append(p1)           
    investor_details1=[investors1,new_loc]
    funding_rounds=[date,funding_amt,funding_rnd,investor_details]
    #convert to csv file
    #output 3 csv files
    if not os.path.exists('Tracxn_'+companyname):
        os.makedirs('Tracxn_'+companyname)
    columns1=['Founded Year','Location','Company Stage','Total Funding','Employee Count','Similar Cos.']
    columns2=['Investors','Location']
    columns3=['Date','Funding Amount','Funding_round','Investor Details']
    df1=pd.DataFrame(overview_values).transpose()
    df1.columns=overview_details
    df1.to_csv('Tracxn_'+companyname+'/'+companyname+'_summary.csv')
    df2=pd.DataFrame(investor_details1).transpose()
    df2.columns=columns2
    df2.to_csv('Tracxn_'+companyname+'/'+companyname+'_investors_details.csv')
    df3=pd.DataFrame(funding_rounds).transpose()
    df3.columns=columns3
    df3.to_csv('Tracxn_'+companyname+'/'+companyname+'_funding_rounds.csv')

    print('CSV DOWNLOADED !')
if __name__=='__main__':
    main(sys.argv[1])
