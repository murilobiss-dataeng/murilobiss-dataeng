import bs4 
import lxml
import sys
import time
import selenium.webdriver.chrome.options	
import selenium.webdriver.chrome.service	
import selenium.webdriver.chrome.webdriver	
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('./src/chromedriver')
time.sleep(5)
driver.get('https://pt.wikipedia.org/wiki/Nicolas_Cage')
tabela = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[2]')
time.sleep(5)
driver.close

df = pd.read_html('<table>' + tabela.get_attribute('innerHTML') + '</table>')[0]

#testando o df
#df
#df[df['Ano']==1984]

df.to_csv('all_movies_nicolas_cage.csv',sep=',', index=False)

