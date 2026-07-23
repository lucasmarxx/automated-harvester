from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient

import time
import os
import csv

# TODO
# criação de classe
# adicionar link das casas
# adicionar função wait



class BuscarCasa:
    def __init__(self):
        self._busca = None
        self._valor_min = None
        self._valor_max = None

    options = Options()
    options.add_argument("--start-maximized")
    # options.page_load_strategy = 'eager'

    driver = webdriver.Chrome(options=options)


    driver.get("https://www.olx.com.br/estado-df")


    # Montando XPATHs (identificadores de elementos)

    # EFETUA PESQUISA NA BARRA DA OLX #
    pesquisa = driver.find_element(
        By.XPATH,
        "//input[@class='olx-core-input-textarea-element olx-core-input-element olx-core-input-textarea-element--default']"
        )

    # pesquisa_wait = WebDriverWait(driver, 20). until(
    #     EC.visibility_of_element_located(By.XPATH,
    #     "//input[@class='olx-core-input-textarea-element olx-core-input-element olx-core-input-textarea-element--default']")
    # )

    if pesquisa:
        pesquisa.click()
        pesquisa.send_keys("Aluguel de casa gama")
        time.sleep(2)
        pesquisa.send_keys(Keys.RETURN)
        time.sleep(2)

    # ---------------------------------------------------------------- #

    # CLICA NO FILTRO RELATIVO A ALUGUEL APENAS DE CASAS #
    filtro_aluguel_casa_apto = driver.find_element(
        By.XPATH, "//p[contains(text(), 'Aluguel')]"
    )
    filtro_aluguel_casa_apto.click()

    time.sleep(2)

    filtro_apenas_casas = driver.find_element(
        By.XPATH, "//*[contains(text(), 'Casas para alugar')]"
    )
    if filtro_apenas_casas:
        filtro_apenas_casas.click()
        time.sleep(2)

    # ---------------------------------------------------------------- #

    # CLICA NO FILTRO RELATIVO À QUANTIDADE DE QUARTOS #

    filtro_quartos = driver.find_element(By.XPATH, "//label[@for = 'chips-id-rooms-3']")

    ActionChains(driver).scroll_to_element(filtro_quartos).perform()
    time.sleep(2)

    if filtro_quartos:
        filtro_quartos.click()
        time.sleep(2)

    # ---------------------------------------------------------------- #


    # CLICA NOS FILTROS DE VALOR MAX E VALOR MIN #
    filtro_valor_min = driver.find_element(By.XPATH, "//input[@id = 'price_min']")
    filtro_valor_max = driver.find_element(By.XPATH, "//input[@id = 'price_max']")

    if filtro_valor_min:
        filtro_valor_min.click()
        filtro_valor_min.send_keys("3000")
        time.sleep(2)

    if filtro_valor_max:
        filtro_valor_max.click()
        filtro_valor_max.send_keys("4000")
        time.sleep(2)

    # ---------------------------------------------------------------- #

    # CLICA NA PESQUISA APÓS FILTROS SEREM PREENCHIDOS #

    botao_pesquisa_filtrado = driver.find_element(
        By.XPATH,
        "//button[@class = 'olx-core-button olx-core-button--primary olx-core-button--small olx-core-button--only-icon FilterButton_filterButton__1P_j9']",
    )
    botao_pesquisa_filtrado.click()

    time.sleep(5)

    # ---------------------------------------------------------------- #

    # PEGA OS NOMES E VALORES DAS CASAS ENCONTRADAS #

    nomes_casas = driver.find_elements(By.XPATH, "//a[@class='olx-adcard__link']")
    valores_casas = driver.find_elements(
        By.XPATH, "//h3[@class = 'typo-body-large olx-adcard__price font-semibold']"
    )

    # ---------------------------------------------------------------- #


    for nome, valor in zip(nomes_casas, valores_casas):
        with open("precos.csv", "a", encoding="utf8") as arquivo:
            arquivo.write(f"{nome.text.split()[0]},{"".join(valor.text.split())}\n") #{os.linesep} 


client = MongoClient('mongodb://localhost:27017')
db = client['Dados_OLX']
colecao = db['colecao_busca_olx']

with open('precos.csv', 'r', encoding = 'utf-8') as arquivo:
    leitor = csv.reader(arquivo)

    dados = []
    for linha in leitor:
        documento = {
            'nome': linha[0],
            'valor': linha[1]
        }
        dados.append(documento)

if dados:
    colecao.insert_many(dados)

# input("") # para o site nao fechar imediatamente