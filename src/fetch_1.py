from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from dotenv import load_dotenv
import schedule
import json
import os
import time
import psycopg2
from psycopg2 import sql



# Carregar variáveis do arquivo .env
load_dotenv()

# URL da API de Produção para obter a última cotação do Bitcoin
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

# Parâmetros da requisição para obter a cotação do Bitcoin
parameters = {
    'symbol': 'BTC',  # Identificando o Bitcoin pelo símbolo
    'convert': 'BRL'  # Convertendo a cotação para real
}

# Headers com a chave da API obtida do arquivo .env
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': os.getenv('CMC_API_KEY'),  # Obtendo a chave do .env
}


# Criar uma sessão
session = Session()
session.headers.update(headers)


response = session.get(url=url, params=parameters)
data = json.loads(response.text)

btc_data = data["data"]["BTC"]
brl_quote = btc_data["quote"]["BRL"]


print(brl_quote["price"])
print(brl_quote["last_updated"])
print(brl_quote["volume_24h"])
print(brl_quote["market_cap"])

