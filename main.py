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

        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://www.olx.com.br/estado-df")
        self.timeout = 10
    # Montando XPATHs (identificadores de elementos)

    # EFETUA PESQUISA NA BARRA DA OLX #
    def pesquisa_inicial(self, busca):
        try:
            # Aguarda campo de pesquisa ficar clicável #
            pesquisa = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable((By.XPATH,
                "//input[@class='olx-core-input-textarea-element olx-core-input-element olx-core-input-textarea-element--default']")
                )
            )
            pesquisa.clear()
            pesquisa.send_keys(busca)
            pesquisa.send_keys(Keys.RETURN)

            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((
                By.XPATH, "//div[contains(@class, 'result') or contains(@class, 'listing')]"
                ))
            )
            print(f'pesquisa "{busca}" realizada com sucesso!')
            return True
        
        except TimeoutException as e:
            print(f'Timeout na pesquisa: {e}')
            return False
        
        except Exception as e:
            print(f'erro na pesquisa: {e}')
            return False
    # ---------------------------------------------------------------- #

    # CLICA NO FILTRO RELATIVO A ALUGUEL APENAS DE CASAS #
    def filtro_casas(self):
        try:
            filtro_aluguel = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable((
                By.XPATH, "//p[contains(text(), 'Aluguel')]")
            ))
            filtro_aluguel.click()
            print('Filtro "Aluguel" clicado!')

            # Aguarda o submenu aparecer
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((
                By.XPATH, "//*[contains(text(), 'Casas para alugar')]"
                ))
            )

            # Clica no filtro 'casas para alugar'
            filtro_apenas_casas = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable((
                By.XPATH, "//*[contains(text(), 'Casas para alugar')]"
            )))
            filtro_apenas_casas.click()
            print('filtro "casas para alugar" clicado!')

            # Aguarda os resultados serem atualizados
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((
                By.XPATH, "//div[contains(@class, 'result') or contains(@class, 'listing')]"
                ))
            )
            return True
        
        except TimeoutException as e:
            print(f'Timeout ao aplicar filtros: {e}')
            return False
        except Exception as e:
            print(f'Erro ao aplicar filtros: {e}')
            return False

    # ---------------------------------------------------------------- #

    # CLICA NO FILTRO RELATIVO À QUANTIDADE DE QUARTOS #
    def filtrar_quartos(self):
            
        filtro_quartos = self.driver.find_element(By.XPATH, "//label[@for = 'chips-id-rooms-3']")

        ActionChains(self.driver).scroll_to_element(filtro_quartos).perform()
        time.sleep(2)

        if filtro_quartos:
            filtro_quartos.click()
            time.sleep(2)

    # ---------------------------------------------------------------- #


    # CLICA NOS FILTROS DE VALOR MAX E VALOR MIN #
    def filtro_valores(self, valor_min, valor_max):
        filtro_valor_min = self.driver.find_element(By.XPATH, "//input[@id = 'price_min']")
        filtro_valor_max = self.driver.find_element(By.XPATH, "//input[@id = 'price_max']")

        if filtro_valor_min:
            filtro_valor_min.click()
            filtro_valor_min.send_keys(valor_min)
            time.sleep(2)

        if filtro_valor_max:
            filtro_valor_max.click()
            filtro_valor_max.send_keys(valor_max)
            time.sleep(2)

    # ---------------------------------------------------------------- #

    # CLICA NA PESQUISA APÓS FILTROS SEREM PREENCHIDOS #
    def botao_pesquisa_final(self):
            
        botao_pesquisa_filtrado = self.driver.find_element(
            By.XPATH,
            "//button[@class = 'olx-core-button olx-core-button--primary olx-core-button--small olx-core-button--only-icon FilterButton_filterButton__1P_j9']",
        )
        botao_pesquisa_filtrado.click()

        time.sleep(5)

    # ---------------------------------------------------------------- #

    # PEGA OS NOMES E VALORES DAS CASAS ENCONTRADAS #
    def pegar_nomes_valores(self):

        nomes_casas = self.driver.find_elements(By.XPATH, "//a[@class='olx-adcard__link']")
        valores_casas = self.driver.find_elements(
            By.XPATH, "//h3[@class = 'typo-body-large olx-adcard__price font-semibold']"
        )

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