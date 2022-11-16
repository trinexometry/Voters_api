#This is a Web Scraping Tool
#That repurposes the website testing tool
#To scrap data of the Voter's List
#From the website of the CEO of Goa
#And Returns a .txt file corrosponding to each constituency's URL
#The Only dependencies the code has are Selenium-4.6.0,MSEdge Driver-107.0.1418.42

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.edge.options import Options

ops = Options()
ops.add_experimental_option('excludeSwitches', ['enable-logging'])

#The current scraper is using MsEdge's driver to run the scraping operation
#To make the code work download the driver of the desired browser in the same folder as that of this program
#Import the appropriate driver function srom the selenium library
#And change the name of the file to that of the driver below

browser = webdriver.Edge(r"msedgedriver.exe",options=ops)

browser.get("https://ceogoa.nic.in/appln/UIL/ElectoralRoll.aspx")

Assembly_consts=browser.find_element(by=By.XPATH,value="//*[@id='ctl00_Main_drpAC']")
Assembly_consts_sel=Select(Assembly_consts)

Search=browser.find_element(by=By.XPATH,value='//*[@id="ctl00_Main_btnSearch"]')

html_code=Assembly_consts.get_attribute("innerHTML")



html_code=html_code[67:]
html_code=html_code.splitlines()

for i in range(0,len(html_code)):
    html_code[i]=html_code[i][16:len(html_code[i])-9]
    html_code[i]=html_code[i].split(sep='">')

html_code=html_code[:-1]


for i in html_code:
    Assembly_consts_sel.select_by_value(i[0])
    Search.click()
    n=3
    try:
        
        while(n):
            pb=browser.find_element(by=By.XPATH,value='//*[@id="'+i[0]+'"]/div['+str(n)+']/a')
            pb.click()
            sleep(5)
            n+=2
    
    except NoSuchElementException:
        
        pdf_urls=[]
        chwk=browser.window_handles
        for w in chwk:
            browser.switch_to.window(w)
            if w==chwk[0]:
                continue
            pdf_urls.append(browser.current_url)
            pdf_urls.append("\n")
            if(len(browser.window_handles)==1):
                break
            browser.close()
        url=open("VotersList-Goa/Goa-"+i[1]+".txt","w")
        url.writelines(pdf_urls)
        url.close()
        browser.switch_to.window(browser.window_handles[0])
    
    except TimeoutException:
        print("...Loading took too long...")

print("...Done Scraping...")
browser.close()
