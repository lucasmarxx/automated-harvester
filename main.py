# Entrar no site - https://www.olx.com.br
# Anotar o nome do primeiro produto
# Anotar o preço do primeiro produto
# Repetir para todos os produtos da página
# Guardar informações em arquivo de texto (csv)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--start-maximized')

driver = webdriver.Chrome(options=options)


driver.get('https://www.olx.com.br')



#Montar o XPATH (identificador de elementos)

# tag = input
# atributo = class 
# valor = texto laranja


pesquisa = driver.find_element(By.XPATH, "//input[@class = 'olx-core-input-textarea-element olx-core-input-element olx-core-input-textarea-element--default']")

if pesquisa:
    pesquisa.click()
    pesquisa.send_keys('Aluguel de casas no gama leste')
    pesquisa.send_keys(Keys.RETURN)

input('') # para o site nao fechar imediatamente