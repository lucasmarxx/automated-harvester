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



# Montando XPATHs (identificadores de elementos)

pesquisa = driver.find_element(By.XPATH, "//input[@class='olx-core-input-textarea-element olx-core-input-element olx-core-input-textarea-element--default']")

if pesquisa:
    pesquisa.click()
    pesquisa.send_keys('Aluguel de casa gama')
    time.sleep(2)
    pesquisa.send_keys(Keys.RETURN)

time.sleep(2)

filtro_aluguel_casa_apto = driver.find_element(By.XPATH, "//p[contains(text(), 'Aluguel')]")
filtro_aluguel_casa_apto.click()

time.sleep(5)

filtro_quartos = driver.find_element(By.XPATH, "//label[@for = 'chips-id-rooms-3']")
filtro_quartos.click()

filtro_valor_min = driver.find_element(By.XPATH, "//input[@id = 'price_min']") 
if filtro_valor_min:
    filtro_valor_min.click()
    filtro_valor_min.send_keys('3000')

time.sleep(2)

filtro_valor_max = driver.find_element(By.XPATH, "//input[@id = 'price_max']")
if filtro_valor_max:
    filtro_valor_max.click()
    filtro_valor_max.send_keys('4000')


time.sleep(5)


input('') # para o site nao fechar imediatamente