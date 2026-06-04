import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "http://quotes.toscrape.com"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' 
}

resposta = requests.get(url, headers=headers)

if resposta.status_code == 200:
    print('Conexão deu certo')

else:
    print(f'falha na conexão. Código: {resposta.status_code}')

print()

if resposta:
    soup = BeautifulSoup(resposta.text, 'html.parser')
    quotes = soup.find_all('div', class_='quote')

    for item, quote in enumerate(quotes, 1):
        texto = quote.find('span', class_='text')
        autor = quote.find('small', class_='author')

        print(f'{item + 1}. \"{texto}\" - {autor}')
    
    dados = []

    for quote in quotes:
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text

        tags = []
        tags_elementos = quote.find_all('a', class_='tag')
        for tag in tags_elementos:
            tags.append(tag.text)

        tags_string = ', '.join(tags)

        dados.append({
            'Frase': text,
            'Autor': author,
            'Tags': tags_string
        })

    df = pd.DataFrame(dados)

    df.to_csv('Citacoes.csv', index=False, encoding = 'utf-8-sig')
    # print(f'\nTotal: {len(quotes)} citações encontradas.')

    print(f'{len(dados)} citações salvas em "citacoes.csv"')
    print('\nPrimeiras 5 citacoes salvas: ')
    print(df.head())

else:
    print(f'Erro ao acessar o site. Código: {resposta.status_code}')

