import json
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import sched
import time
from datetime import datetime

event_schedule = sched.scheduler(time.time, time.sleep)
myclient = MongoClient('mongodb://192.168.1.216:27017/db?authSource=admin')

#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--disable-gpu')
#driver = webdriver.Chrome(chrome_options=chrome_options)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(executable_path = 'C:/Webdrivers/chromedriver.exe', chrome_options = chrome_options)

def insert_order_info(info, number):
    date = ''
    x = myclient.ctt_tracking.orders_info.find({'number': number}).sort('scrapt_date', -1).limit(1)
    last = None
    for u in x:
        if len (u) > 0: 
                last = u
        else:
            last = None

    for td in info:
        if "group" in td.get_attribute("class"):
            date = td.text
        else:
            if len(td.text.split()) > 0:
                if (last == None) or (last['data'] != date and last['hora'] != td.find_elements_by_xpath(".//*")[0].text):
                    now = datetime.now()
                    info = {
                        "number": number,
                        "data": date,
                        "hora": td.find_elements_by_xpath(".//*")[0].text,
                        "estado": td.find_elements_by_xpath(".//*")[1].text,
                        "motivo": td.find_elements_by_xpath(".//*")[2].text,
                        "local": td.find_elements_by_xpath(".//*")[3].text,
                        "recetor": td.find_elements_by_xpath(".//*")[4].text,
                        "recetor": td.find_elements_by_xpath(".//*")[4].text,
                        "scrapt_date": now.strftime("%d/%m/%Y %H:%M:%S")
                    }
                    myclient.ctt_tracking.orders_info.insert_one(info)

def do_tracking_to_order(number):
    driver.get('https://www.ctt.pt/feapl_2/app/open/objectSearch/objectSearch.jspx')
    search_field = driver.find_element_by_id('objects')
    search_field.send_keys(number)
    driver.find_element_by_id('searchButton').click()
    WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.ID, 'detailsLinkShow_0')))
    WebDriverWait(driver, 45).until(EC.element_to_be_clickable((By.ID, 'detailsLinkShow_0')))
    driver.find_element_by_id('detailsLinkShow_0').click()
    WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.XPATH, '//*[@id="details_0"]/td/div/table/tbody')))
    table_tracking = driver.find_elements(By.XPATH, '//*[@id="details_0"]/td/div/table/tbody/tr')
    insert_order_info(table_tracking, number)
    driver.close()
    driver.quit()

def do_tracking():
    for order in myclient.ctt_tracking.orders.find():
        if order['received'] == bool(False):
            print ('Check order: ' + order['number'])
            do_tracking_to_order(order['number'])

do_tracking()
#event_schedule.enter(30, 1, do_tracking, ('second',))
#event_schedule.run()