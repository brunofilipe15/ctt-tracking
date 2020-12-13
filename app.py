import json
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

#myclient = MongoClient('mongodb://192.168.1.216:27017/db?authSource=admin')
#print(myclient.server_info())

#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--disable-gpu')
#driver = webdriver.Chrome(chrome_options=chrome_options)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(executable_path = 'C:/Webdrivers/chromedriver.exe', chrome_options = chrome_options)
driver.get('https://www.ctt.pt/feapl_2/app/open/objectSearch/objectSearch.jspx')
search_field = driver.find_element_by_id('objects')
search_field.send_keys('DW108338622PT')
driver.find_element_by_id('searchButton').click()
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'detailsLinkShow_0')))
driver.find_element_by_id('detailsLinkShow_0').click()
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="details_0"]/td/div/table/tbody')))
table_tracking = driver.find_elements(By.XPATH, '//*[@id="details_0"]/td/div/table/tbody/tr')

for td in table_tracking:
    print("group" in td.get_attribute("class"))
    print(td.text)

#.split()
#print(table_tracking[8])

#ultima_atualizacao = {
#  "idx": table_tracking[8],
#  "data": table_tracking[10],
#  "hora": table_tracking[11],
#  "info": table_tracking[12] + ' ' + table_tracking[13]
#}
#myclient.ctt_tracking.orders.insert_one(ultima_atualizacao)
driver.close()
driver.quit()