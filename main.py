# Entrar no site - https://www.olx.com.br
# Anotar o nome do primeiro produto
# Anotar o preço do primeiro produto
# Repetir para todos os produtos da página
# Guardar informações em arquivo de texto (csv)

from selenium import webdriver

driver = webdriver.Chrome()

driver.get('https://www.olx.com.br')
input('') # para o site nao fechar imediatamente
