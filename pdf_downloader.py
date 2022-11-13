from selenium import webdriver
from selenium.webdriver.edge.options import Options
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select

browser = webdriver.Edge(r"msedgedriver.exe")

browser.get("https://ceogoa.nic.in/appln/UIL/ElectoralRoll.aspx")

Assembly_consts=browser.find_element(by=By.XPATH,value="//*[@id='ctl00_Main_drpAC']")
Assembly_consts_sel=Select(Assembly_consts)
Search=browser.find_element(by=By.XPATH,value='//*[@id="ctl00_Main_btnSearch"]')

html_code=Assembly_consts.get_attribute("innerHTML")

Const_Dict={}

html_code=html_code[67:]
html_code=html_code.splitlines()

for i in range(0,len(html_code)):
    html_code[i]=html_code[i][16:len(html_code[i])-9]
    html_code[i]=html_code[i].split(sep='">')
html_code=html_code[:-1]

pdf_urls=[]

for i in html_code:
    Assembly_consts_sel.select_by_value(i[0])
    Search.click()
    n=3
    try:
        pb=browser.find_element(by=By.XPATH,value='//*[@id="'+i[0]+'"]/div['+str(n)+']/a')
        pb.click()
        sleep(7)
        n+=2
    except:
        chwk=browser.window_handles
        for w in chwk:
            if w!=chwk[0]:
                if(w!=browser.current_window_handle()):
                    browser.switch_to.window(w)
                    pdf_urls.append(browser.current_url)
        url=open(i[1]+".txt","w")
        for i in pdf_urls:
            inp_str=i+"\n"
        inp_str=inp_str[:-1]
        url.write(inp_str)
        continue
