from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from dotenv import load_dotenv
import schedule
import json
import os
import time

# Carregar variáveis do arquivo .env
load_dotenv()

# URL da API de Produção para obter a última cotação do Bitcoin
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

# Parâmetros da requisição para obter a cotação do Bitcoin
parameters = {
    'symbol': 'BTC',  # Identificando o Bitcoin pelo símbolo
    'convert': 'BRL'  # Convertendo a cotação para USD
}

# Headers com a chave da API obtida do arquivo .env
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': os.getenv('CMC_API_KEY'),  # Obtendo a chave do .env
}

# Criar uma sessão
session = Session()
session.headers.update(headers)

# Função que faz a requisição à API e imprime a última cotação do Bitcoin
def consultar_cotacao_bitcoin():
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        
        # Verificar se os dados do Bitcoin estão presentes na resposta
        if 'data' in data and 'BTC' in data['data']:
            bitcoin_data = data['data']['BTC']
            brl_quote = bitcoin_data['quote']['BRL']
            
            # Imprimir os dados da cotação
            print(f"Última cotação do Bitcoin: ${brl_quote['price']:.2f} BRL")
            print(f"Volume 24h: ${brl_quote['volume_24h']:.2f} BRL")
            print(f"Market Cap: ${brl_quote['market_cap']:.2f} BRL")
            print(f"Última atualização: {brl_quote['last_updated']}")
        else:
            print("Erro ao obter a cotação do Bitcoin:", data['status'].get('error_message', 'Erro desconhecido'))

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(f"Erro na requisição: {e}")

# Agendar a função para rodar a cada 15 segundos
schedule.every(15).seconds.do(consultar_cotacao_bitcoin)

# Loop principal para manter o agendamento ativo
if __name__ == "__main__":
    print("Iniciando o agendamento para consultar a API a cada 15 segundos...")
    while True:
        schedule.run_pending()
        time.sleep(1)