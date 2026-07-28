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

            time.sleep(1)
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
            filtro_valor_max.submit()
            
        except TimeoutException as e:
            print(f'Timeout ao filtrar valor: {e}')
            return False
        except Exception as e:
            print(f'Erro ao filtrar valores: {e}')

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
        


        
    def fechar(self):
        if self.driver:
            self.driver.quit()
            print('navegador fechado!')


# Classe para integração com banco de dados

class BancoDados:
    def __init__(self):
        try:
            self.client = MongoClient('mongodb://localhost:27017')
            self.db = self.client['Dados_OLX']
            self.colecao = self.db['colecao_busca_olx']
            print('conectado ao mongodb com sucesso')
        except Exception as e:
            print(f'erro ao conectar-se ao mongodb: {e}')

    def integrar_bancos(self):
        ...

    def fechar_conexao(self):
        if self.client:
            self.client.close()
            print('fechando conexao com mongodb!')
    
        # with open('precos.csv', 'r', encoding = 'utf-8') as arquivo:
        #             leitor = csv.reader(arquivo)
        
        #             dados = []
        #             for linha in leitor:
        #                 documento = {
        #                     'nome': linha[0],
        #                     'valor': linha[1],
        #                     'link': linha[2]
        #                 }
        #                 dados.append(documento)
        
        # if dados:
        #     self.colecao.insert_many(dados)



if __name__ == '__main__':
    buscador = BuscarCasa()
    banco = BancoDados()

    anuncios_links = []
    anuncios_nomes = []
    anuncios_valores = []
    try:
        buscador.pesquisa_inicial('ALUGUEL DE CASAS NO GAMA') # BUSCA
        buscador.filtro_casas()
        buscador.filtrar_quartos()
        buscador.filtro_valores(2500, 4500) # VALORES
        dados = buscador.pegar_nomes_valores()
        banco.integrar_bancos()
        print('\n Links dos Anúncios: ')
        for dado in dados:
            anuncios_links.append(dado['link'])
            anuncios_nomes.append(dado['nome'])
            anuncios_valores.append(dado['valor'])
            print(f'Anúncio {dado['numero']}: {dado['link']}')

        for nome, valor, link in zip(anuncios_nomes, anuncios_valores, anuncios_links):
            with open("precos.csv", "a", encoding="utf8") as arquivo:
                arquivo.write(f'{nome.split()[0]},{"".join(valor.split())},{link}\n') #{os.linesep} 

    except Exception as e:
        print(f'Erro geral: {e}')

    finally:
        buscador.fechar()
        banco.fechar_conexao()