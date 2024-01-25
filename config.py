import requests
import Teste as TT 
from datetime import datetime,timedelta
Token = TT.get_token('victor.drone2013@gmail.com','899513Vi!')


header = {"Access-Token": Token}
data_atual=datetime.today()
data_inicio= (datetime.today()- timedelta(days=1))
data_fim = data_atual
dados = requests.get('https://api.oplab.com.br/v3/market/historical/options/{}/{}/{}'
                    .format('PETR4', data_inicio.strftime("%Y%m%d%H%M"),
                    data_fim.strftime("%Y%m%d%H%M")),headers=header).json()
for i in range(0,400):

    rimeiro_simbolo = dados[i]['symbol']
    preco_apple = dados[i]['type']
    print(rimeiro_simbolo,preco_apple)
    i+1