from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = 'https://www.ctt.pt/feapl_2/app/open/cttexpresso/objectSearch/objectSearch.jspx'
driver = webdriver.Chrome('./chromedriver')
print(driver.title)