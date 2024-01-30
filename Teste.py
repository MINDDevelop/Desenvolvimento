from datetime import datetime
import requests
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings
from datetime import datetime,timedelta
import imageio
import os
from matplotlib import style
from workalendar.america import Brazil


warnings.simplefilter('ignore', np.RankWarning)


pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

### FUNÇÃO PARA PEGAR TOKEN DE AUTENTICAÇÃO NA API
def get_token(email,senha):
    ## BODY PARA REQUISIÇÃO NA API
    body = {"email": email,"password": senha}
    
    ## CHAMADA NA API
    r = requests.post('https://api.oplab.com.br/v3/domain/users/authenticate',json=body).json()['access-token']
    return r

def opcoes_ativos(Token,symbol):
    from workalendar.america import Brazil
    header = {"Access-Token": Token}
    cal=Brazil()
    hoje = datetime.now().date()
    data_atual= datetime.now().date()
     # Verificar se hoje é um feriado ou fim de semana
    while not cal.is_working_day(hoje) or hoje.weekday() == 0 or hoje.weekday() >= 5:
        # Se for feriado, segunda-feira ou fim de semana, subtrair 1 dia
        hoje -= timedelta(days=1)

    # Agora hoje é um dia útil
    util_anterior = hoje - timedelta(days=1)
    
    ## CHAMADA NA API 
    dados = requests.get('https://api.oplab.com.br/v3/market/options/{}'.format(symbol),headers=header).json()
    columns= ['symbol', 'block_date', 'category', 'contract_size', 
              'days_to_maturity', 'due_date', 'exchange_id', 'isin',
                'market_maker', 'maturity_type', 'name', 'strike', 'updated_at',
                  'close', 'created_at', 'financial_volume', 'high', 'low', 'open',
                    'variation', 'volume', 'ask', 'bid', 'quotationForm', 'security_category', 
                    'spot_price', 'trades', 'cnpj', 'lastUpdatedDividendsAt', 'time', 'type', 
                    'last_trade_at', 'strike_eod']
    df=pd.DataFrame(dados,columns=columns)
    df_filtrado=df[['symbol','category','days_to_maturity','strike','ask','bid','volume','due_date']]
    dados = requests.get('https://api.oplab.com.br/v3/market/historical/options/{}/{}/{}'.format(symbol, util_anterior.strftime("%Y%m%d%H%M"), data_atual.strftime("%Y%m%d%H%M")),
                   headers=header).json()
    df_moneyness=pd.DataFrame(dados)
    df_moneyness = df_moneyness[['symbol','moneyness']]
    df_final = pd.merge(df_filtrado, df_moneyness, how='inner', on='symbol')
    df_final = df_final.drop_duplicates(subset=['symbol','due_date','category',],keep='first')
    return df_final

def Cotacoes(Token,symbol):
    header = {"Access-Token": Token}
    
    ## CHAMADA NA API 
    dados = requests.get('https://api.oplab.com.br/v3/market/stocks/{}'.format(symbol),headers=header).json()  
    if dados.get('spot_price', None)=='':
        preco=dados.get('spot_price', None)
    else:
        preco=dados.get('close',None) 
    return preco

