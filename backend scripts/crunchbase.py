from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os,random,sys,time
import pandas as pd
import re
from re import search
# give the company name
def main(companyname):
    chrome_path="C:\\Users\\Taha\\Desktop\\chromedriver.exe"
    driver=webdriver.Chrome(chrome_path)
    driver.get('https://www.crunchbase.com/discover/organization.companies/')
    req=driver.find_element_by_xpath("""//*[@id="mat-input-0"]""")
    req.send_keys(companyname)
    driver.find_element_by_xpath("""//*[@id="mat-input-0"]""").send_keys(Keys.ENTER)
    companypath='https://www.crunchbase.com/organization/'+companyname.lower()
    driver.get(companypath)
    #about details
    about=[]
    time.sleep(8)
    e=driver.find_element_by_xpath("""/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/ng-component/entity-v2/page-layout/div/div/div/page-centered-layout[2]/div/row-card/div/div[1]/profile-section/section-card/mat-card/div[2]/div/fields-card/ul""")
    k=e.find_elements_by_tag_name('li')
    for tag in k:
        about.append(tag.text)
    #print(about)
    #Details
    details_name=[]
    details_values=[]
    time.sleep(5)
    e=driver.find_element_by_xpath("""/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/ng-component/entity-v2/page-layout/div/div/div/page-centered-layout[3]/div/div/div[1]/row-card[1]/profile-section/section-card/mat-card/div[2]/div/fields-card[1]/ul""")
    k=e.find_elements_by_tag_name('li')
    for tag in k:
        ele1=tag.find_element_by_tag_name('label-with-info')
        ele2=tag.find_elements_by_tag_name('field-formatter')
        details_name.append(ele1.text)
        l=[]
        for values in ele2:
            l.append(values.text)
        details_values.append(l)
    #print(details_name)
    #print(details_values)
    #email and phone path
    time.sleep(5)
    email=''
    phone=''
    try:
        email=driver.find_element_by_xpath("""/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/ng-component/entity-v2/page-layout/div/div/div/page-centered-layout[3]/div/div/div[1]/row-card[1]/profile-section/section-card/mat-card/div[2]/div/fields-card[3]/ul/li/field-formatter/blob-formatter/span""").text
    except:
        email='Not available'
    try:
        phone=driver.find_element_by_xpath("""/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/ng-component/entity-v2/page-layout/div/div/div/page-centered-layout[3]/div/div/div[1]/row-card[1]/profile-section/section-card/mat-card/div[2]/div/fields-card[4]/ul/li[2]/field-formatter/blob-formatter/span""").text
    except:
        phone='Not available'
    #Technology
    techpath=companypath+'/technology'
    driver.get(techpath)
    time.sleep(5)
    technology_names=[]
    technology_values=[]
    e1=driver.find_element_by_xpath("""/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/ng-component/entity-v2/page-layout/div/div/div/page-centered-layout[2]/div/row-card/div/div[1]/profile-section/section-card/mat-card/div[2]/div/anchored-values""")
    k1=e1.find_elements_by_tag_name('a')
    for tag in k1:
        technology_names.append(tag.find_element_by_tag_name('label-with-info').text)
        technology_values.append(tag.find_element_by_tag_name('field-formatter').text)
    #print(technology_names)
    #print(technology_values)
    #Signal and News
    #time.sleep(20)
    #let us extract to 20 articles
    #count=0
    #signalpath=companypath+'/signals_and_news/timeline'
    #driver.get(signalpath)
    #signal_path=[]
    #w=driver.find_elements_by_xpath("""/html/body/chrome/div/mat-sidenav-container/mat-sidenav-content/div/ng-component/entity-v2/page-layout/div/div/div/page-centered-layout[2]/div/profile-section/section-card/mat-card/div[2]/div/timeline-card""")
    #for tag in w:
    #        q=tag.find_elements_by_tag_name('div')
    #        while(count<20):
    #            for tag2 in q:
    #                x=tag2.find_element_by_class_name('activity-details')
    #                signal_path.append(x.text)
    #                count+=1
    
    #write_to_csv
    founded_date=''
    founders=''
    website=''
    total_product_active=''
    active_tech_count=''
    monthly_visits=''
    monthly_visits_growth=''
    for i in range(0,len(details_name)):
        if(details_name[i]=='Founders '):
            founders=details_values[i][0]
        if(details_name[i]=='Founded Date '):
            founded_date=details_values[i][0]
    for values in about:
        if(re.search('.com',values)):
            website=values
    for i in range(0,len(technology_names)):
        if(technology_names[i]=='Total Products Active '):
            total_product_active=technology_values[i]
        if(technology_names[i]=='Active Tech Count '):
            active_tech_count=technology_values[i]
        if(technology_names[i]=='Monthly Visits '):
            monthly_visits=technology_values[i]
        if(technology_names[i]=='Monthly Visits Growth '):
            monthly_visits_growth=technology_values[i]
    Industries=''
    for i in range(0,len(details_name)):
        if(details_name[i]=='Industries '):
            lister=details_values[i][0].split('\n')
            Industries=','.join(lister)
    lists=[about[0],email,phone,founders,founded_date,Industries,website,about[1],total_product_active,active_tech_count,monthly_visits,monthly_visits_growth]
    columns=['Location','EmailId','PhoneNo','Founders','Founded Date','Industries','Website','Size of Company','Total Products Active','Active Tech Count','Monthly Visits','Monthly Visits Growth']
    df=pd.DataFrame(lists).transpose()
    df.columns=columns
    df.to_csv('crunchbase_'+companyname+'.csv')
    #columns1=['Signals and news']
    #df1=pd.DataFrame(signal_path)
    #df1.columns=columns1
    #df1.to_csv(companyname+'_signals_and_news.csv')
 
    print('CSV DOWNLOADED !')
if __name__ == '__main__':
    main(sys.argv[1])
