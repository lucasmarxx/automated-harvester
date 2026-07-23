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
        self.wait = WebDriverWait(self.driver, self.timeout)
        self.actions = ActionChains(self.driver)


    # EFETUA PESQUISA NA BARRA DA OLX #
    def pesquisa_inicial(self, busca):
        try:
            # Aguarda campo de pesquisa ficar clicável #
            pesquisa = self.wait.until(
                EC.element_to_be_clickable((By.XPATH,
                "//input[@class='olx-core-input-textarea-element olx-core-input-element olx-core-input-textarea-element--default']")
                )
            )
            pesquisa.clear()
            pesquisa.send_keys(busca)
            time.sleep(1)
            pesquisa.submit()

            self.wait.until(
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
            self.wait.until(
                EC.presence_of_element_located((
                By.XPATH, "//div[contains(@class, 'listing') or contains(@class, 'result')]"
                ))
            )
            return True
        
        except TimeoutException as e:
            print(f'Timeout ao aplicar filtros: porraaaaaaaaaaaaaaaaa {e}')
            return False
        
        except Exception as e:
            print(f'Erro ao aplicar filtros: {e}')
            return False

        
    def filtrar_quartos(self):
        try:
            # Aguarda o elemento estar presente no DOM
            filtro_quartos = self.wait.until(
                EC.presence_of_element_located((
                By.XPATH, "//label[@for = 'chips-id-rooms-3']" ))
            )

            # Scroll até o elemento para garantir visibilidade
            self.actions.scroll_to_element(filtro_quartos).perform()
            print('Scroll até o filtro de 3 quartos!')


            # Aguarda elemento estar clicável
            self.wait.until(
                EC.element_to_be_clickable((
                By.XPATH, "//label[@for = 'chips-id-rooms-3']" 
                ))
            )

            # Verifica se está selecionado
            # is_checked = filtro_quartos.get_attribute('checked')
            # if is_checked:
            #     print('Filtro de 3 quartos devidamente selecionado')
            #     return True
            
            filtro_quartos.click()
            print('filtro de 3 quartos aplicado')

            time.sleep(2)
            return True
        
        except TimeoutException as e:
            print(f'Timeout ao filtrar 3 quartos: {e}')
            return False
        except Exception as e:
            print(f'Erro ao filtrar 3 quartos: {e}')
            return False

    # ---------------------------------------------------------------- #


    # CLICA NOS FILTROS DE VALOR MAX E VALOR MIN #
    def filtro_valores(self, valor_min, valor_max):
        try:
            filtro_valor_min = self.wait.until(
                EC.element_to_be_clickable((
                By.XPATH, "//input[@id = 'price_min']"))
                )
            filtro_valor_max = self.wait.until(
                EC.element_to_be_clickable((
                By.XPATH, "//input[@id = 'price_max']"))
                )

            filtro_valor_min.send_keys(valor_min)
            print(f'Valor mínimo >>{valor_min}<< adicionado ao filtro')
            time.sleep(1)
            filtro_valor_max.send_keys(valor_max)
            print(f'Valor maximo >>{valor_max}<< adicionado ao filtro')
            time.sleep(10)
            
        except TimeoutException as e:
            print(f'Timeout ao filtrar valor: {e}')
            return False
        except Exception as e:
            print(f'Erro ao filtrar valores: {e}')


    # ---------------------------------------------------------------- #

    # CLICA NA PESQUISA APÓS FILTROS SEREM PREENCHIDOS #
    def botao_pesquisa_final(self):
        try:    
            botao_pesquisa_filtrado = self.wait.until(
                EC.presence_of_element_located((
                By.XPATH,
                "//button[@class = 'olx-core-button olx-core-button--primary olx-core-button--small olx-core-button--only-icon FilterButton_filterButton__1P_j9']",
                ))
                )
            botao_pesquisa_filtrado.click()
            print('Botão de pesquisa clicado!!')
            time.sleep(5)

        except TimeoutException as e:
            print(f'Timeout no botão de pesquisa: {e}')
            return False
        except Exception as e:
            print(f'Erro no botão de pesquisa: {e}')
            return False
    # ---------------------------------------------------------------- #

    # PEGA OS NOMES E VALORES DAS CASAS ENCONTRADAS #
    def pegar_nomes_valores(self):
        try:
            nomes_casas = self.driver.find_elements(By.XPATH, "//a[@class='olx-adcard__link']")
            valores_casas = self.driver.find_elements(
                By.XPATH, "//h3[@class = 'typo-body-large olx-adcard__price font-semibold']"
            )
            # Verifica se encontrou elementos
            if not nomes_casas:
                print('Nenhum anúncio encontrado')
                return []

            anuncios = []

            for i, (nome, valor) in enumerate(zip(nomes_casas, valores_casas), 1):
                try:
                    link = nome.get_attribute('href')

                    nome_texto = nome.text.strip() if nome.text else 'Nome não encontrado'

                    valor_texto = valor.text.strip() if valor.text else 'Valor não encontrado'

                    anuncios.append({
                    'numero': i,
                    'nome': nome_texto,
                    'valor': valor_texto,
                    'link': link
                })

                    print(f'Anuncio {i}:')
                    print(f'Nome: {nome_texto}')
                    print(f'Valor: {valor_texto}')
                    print(f'Link: {link}')

                except Exception as e:
                    print(f'ERRO AO PROCESSAR ANUNCIO {i}: {e}')
                    continue
            
            print(f'{len(anuncios)} anuncios processados com sucesso.')
            return anuncios
        except Exception:
            print(f'Erro ao pegar nomes e valores: {e}')
            return []
        


            # self.driver.find_elements(By.XPATH, "//a[@class='olx-adcard__link']")

            # for nome, valor in zip(nomes_casas, valores_casas):
            #     with open("precos.csv", "a", encoding="utf8") as arquivo:
            #         arquivo.write(f"{nome.text.split()[0]},{"".join(valor.text.split())}\n") #{os.linesep} 

        
    def fechar(self):
        if self.driver:
            self.driver.quit()
            print('navegador fechado!')


if __name__ == '__main__':
    buscador = BuscarCasa()

    try:
        buscador.pesquisa_inicial('ALUGUEL DE CASAS NO GAMA') # BUSCA
        buscador.filtro_casas()
        buscador.filtrar_quartos()
        buscador.filtro_valores(2500, 4500) # VALORES
        buscador.botao_pesquisa_final()
        anuncios = buscador.pegar_nomes_valores()
        print('\n Links dos Anúncios: ')
        for anuncio in anuncios:
            print(f'Anúncio {anuncio['numero']}: {anuncio['link']}')
        
    except Exception as e:
        print(f'Erro geral: {e}')

    finally:
        buscador.fechar()

# Classe para integração com banco de dados

class BancoDados:
    def __init__(self):

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