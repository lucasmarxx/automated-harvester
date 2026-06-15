from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--start-maximized')
# options.page_load_strategy = 'eager'

driver = webdriver.Chrome(options=options)


driver.get('https://www.olx.com.br/estado-df')



# Montar o XPATH (identificador de elementos)

pesquisa = driver.find_element(By.XPATH, "//input[@class='olx-core-input-textarea-element olx-core-input-element olx-core-input-textarea-element--default']")

if pesquisa:
    pesquisa.click()
    pesquisa.send_keys('Aluguel de casas gama')
    time.sleep(2)
    pesquisa.send_keys(Keys.RETURN)

time.sleep(2)

filtro_valor_min = driver.find_element(By.XPATH, "//input[@id = 'price_min']") 
if filtro_valor_min:
    filtro_valor_min.click()
    filtro_valor_min.send_keys('3000')

time.sleep(2)

filtro_valor_max = driver.find_element(By.XPATH, "//input[@id = 'price_max']")
if filtro_valor_max:
    filtro_valor_max.click()
    filtro_valor_max.send_keys('4000')

time.sleep(2)

botao_pesquisar = driver.find_element(By.XPATH, "//button[@aria-label='aplicar filtro Preço']")
botao_pesquisar.click()

time.sleep(5)

filtro_casas_e_aptos = driver.find_element(By.XPATH, "//svg[@xmlns='http://www.w3.org/2000/svg']")
filtro_casas_e_aptos.click()

time.sleep(5)

input('') # para o site nao fechar imediatamente