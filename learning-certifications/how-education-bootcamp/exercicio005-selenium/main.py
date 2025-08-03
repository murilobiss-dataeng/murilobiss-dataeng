import sys
import time
import selenium.webdriver.chrome.options	
import selenium.webdriver.chrome.service	
import selenium.webdriver.chrome.webdriver	
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

cep = sys.argv[1]

if cep:
    driver = webdriver.Chrome('./src/chromedriver')
    time.sleep(10)
    driver.get('https://buscacepinter.correios.com.br/app/endereco/index.php?t')
    elem_cep = driver.find_element(By.XPATH,'//*[@id="endereco"]')

    elem_cep.clear()
    elem_cep.send_keys('82900010')

    #Preenchendo Formulário
    #Opções
    # [1] Localidade/Logradouro
    # [2] CEP Promocional
    # [3] Caixa Postal Comunitária
    # [4] Grande Usuário
    # [5] Unidade Operacional
    # [6] Todos

    elem_cmb = driver.find_element(By.NAME,'tipoCEP')
    elem_cmb.click()
    driver.find_element(By.XPATH,'//*[@id="tipoCEP"]/optgroup/option[6]').click()
    driver.find_element(By.ID, 'btn_pesquisar').click()
    time.sleep(10)
    logradouro = driver.find_element(By.XPATH, '//*[@id="resultado-DNEC"]/tbody/tr/td[1]').text
    bairro = driver.find_element(By.XPATH,'//*[@id="resultado-DNEC"]/tbody/tr/td[2]').text
    localidade = driver.find_element(By.XPATH,'//*[@id="resultado-DNEC"]/tbody/tr/td[3]').text
    
    driver.close()

    print('''
    Para o Cep {}, temos:
    Endereço: {}
    Bairro: {}
    Localidade: {}
    '''.format(
    cep,
    logradouro.split(' - ')[0],
    bairro,
    localidade))
