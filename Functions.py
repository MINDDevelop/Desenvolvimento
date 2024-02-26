from datetime import datetime
import requests
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings
from datetime import datetime,timedelta
import cacluldora_BS as BS
import os
from matplotlib import style
from workalendar.america import Brazil
import xml.etree.ElementTree as ET



########################################################################################################
def get_token(email,senha): #OK
    
    body = {"email": email,"password": senha}
    
    ## CHAMADA NA API
    r = requests.post('https://api.oplab.com.br/v3/domain/users/authenticate',json=body).json()['access-token']
    return r

email='victor.drone2013@gmail.com'
senha='899513Vi!'
Token=get_token(email,senha)
########################################################################################################

def opcoes_ativos(symbol): #OK
    """
    symbol= ticker da ação que queremos ver as opções

    Retorna:
    - todos as opções que temos dessa opção, com seu simbolo, categoria, strike, vencimento, preços do book

    """
    header = {"Access-Token": Token}
    dados = requests.get('https://api.oplab.com.br/v3/market/options/{}'.format(symbol),headers=header).json()
    columns= ['symbol', 'category', 
               'due_date', 
                'strike', 
                'volume', 'ask', 'bid',
                 'type']
    df=pd.DataFrame(dados,columns=columns)
    
    return df
##########################################################################################################
def Cotacoes(symbol):  #OK
    """
    symbol= ticker da ação que queremos ver as opções

    Retorna:
    - pegamos a cotação do ativo. caso o mercado esteja fechado usamos o ultimo preço de fechamento do ativo

    """
    header = {"Access-Token": Token}
    
    ## CHAMADA NA API 
    dados = requests.get('https://api.oplab.com.br/v3/market/stocks/{}'.format(symbol),headers=header).json()  
    if dados.get('spot_price', None)=='':
        preco=dados.get('spot_price', None)
    else:
        preco=dados.get('close',None) 
    return preco
##########################################################################################################

def Cotação_historica(symbol,_from,_to,resolution="1d",df="iso"):
    """
    symbol= ticker da ação que queremos ver as opções
    _from=a partir de quando vc quer ver o historico
    _to= até quando se quer o historico
    resolution= está configurando para pegar a cotação diária mas é possivel definir outra configuração 
    padrão de data "2024-02-19T00:00:00"
    Retorna:
    - Cotação Historica do ativo

    """
    header = {"Access-Token": Token}
    dados=requests.get(rf'https://api.oplab.com.br/v3/market/historical/{symbol}/{resolution}?from={_from}&to={_to}&df={df}',
                       headers=header).json()
    df=pd.DataFrame(dados)
    df['time']=df['data'].apply(lambda x: x['time'])
    
    df['close']=df['data'].apply(lambda x: x['close'])
    return df[['symbol','time','close']]
##########################################################################################################

def determinar_tmoney(row):
    if row['strike'] > row['close']:
        return 'OTM'
    else:
        return 'ITM'
def determinar_tmoney2(row):
    if row['p.strike']<=6:
        return 'ATM'
    if row['strike'] > row['Preco_ativo']:
        return 'OTM'
    else:
        return 'ITM'
##########################################################################################################
 

def Consultas_opção(symbol):
    header = {"Access-Token": Token}
    dados = requests.get('https://api.oplab.com.br/v3/market/options/details/{}'.format(symbol),headers=header).json()
    colunas_desejadas = ['symbol', 'strike', 'type','due_date','spot_price','parent_symbol','bid','ask']
    df=pd.DataFrame([dados],columns=colunas_desejadas)
# Criar um novo dicionário contendo apenas as colunas desejadas
    
    
    return df
##########################################################################################################


def ccotacao_determinada(tickers,date):
    
    header = {"Access-Token": Token}
    dados=requests.get(rf'https://api.oplab.com.br/v3/market/historical/instruments?tickers={tickers}&date={date}',
                       headers=header).json()
    return dados

def acertar_data(data):
    data_usar=data/1000
    Data_certa = datetime.utcfromtimestamp(data_usar)
    return Data_certa

def cotacoao(Ticker):
    cal=Brazil()
    hoje = datetime.now().date()
    data_atual= datetime.now().date()
    pd.set_option('display.width', 1000)
    cotacao=Cotação_historica(Ticker,(data_atual-timedelta(1)),data_atual)
    dados=pd.DataFrame(cotacao)
    dados['spot']=dados['data'].apply(lambda x:x['close'])
    dados['data']=dados['data'].apply(lambda x:x['time'])
    dados['data']=dados['data'].apply(acertar_data)
    dados['data']=dados['data']-timedelta(hours=3)
    
  
    dados=dados.drop(columns=['name','resolution'])
    dados['data'] = pd.to_datetime(dados['data'])
    dados['data'] = dados['data'].dt.strftime('%H:%M:%S')
    dados=dados.rename(columns={
    'data': 'Hora',
    })
    return dados



def acoes_options():
    header = {"Access-Token": Token}
    dados = requests.get('https://api.oplab.com.br/v3/market/stocks',headers=header).json()  
    df=pd.DataFrame(dados)
    df=df[df['has_options']==True]
    return df[['symbol','close']]



def Consultas_ativo(symbol):
    header = {"Access-Token": Token}
    dados = requests.get('https://api.oplab.com.br/v3/market/options/details/{}'.format(symbol),headers=header).json()
    colunas_desejadas = ['parent_symbol']

# Criar um novo dicionário contendo apenas as colunas desejadas
    novo_dados = {coluna: dados[coluna] for coluna in colunas_desejadas}
    return novo_dados


def determinar_tmoney3(row):
    if row['p.strike']<=6:
        return 'ATM'
    else:
        return None



def nova_funcao(symbol,util_anterior,data_atual):
    header = {"Access-Token": Token}
    dados = requests.get('https://api.oplab.com.br/v3/market/historical/options/{}/{}/{}'.format(symbol, util_anterior.strftime('%Y-%m-%d'), data_atual.strftime('%Y-%m-%d')),
                   headers=header).json()
    df=pd.DataFrame(dados)
    df=df[['symbol','spot','type']]
    df['spot']=df['spot'].apply(lambda x: x['symbol'])
    return df
  
def funcao_para_atm_ask(row):
    if row['tmoney'] == 'ATM':
        row['VI_ask']=row.apply(BS.calcular_IV_hist_ask, axis=1)
        row['VI_bid']=row.apply(BS.calcular_IV_hist_ask, axis=1)
    else:
        row['VI_ask']= ''
        row['VI_bid'] = ''

def Consultas_opção_venc(symbol):
    header = {"Access-Token": Token}
    dados = requests.get('https://api.oplab.com.br/v3/market/options/details/{}'.format(symbol),headers=header).json()
    vencimento=dados['due_date']
    # df=pd.DataFrame((dados),columns=colunas_desejadas)
# Criar um novo dicionário contendo apenas as colunas desejadas
    return vencimento
def Consultas_opção_strike(symbol):
    header = {"Access-Token": Token}
    dados = requests.get('https://api.oplab.com.br/v3/market/options/details/{}'.format(symbol),headers=header).json()
    strike=dados['strike']
    # df=pd.DataFrame((dados),columns=colunas_desejadas)
# Criar um novo dicionário contendo apenas as colunas desejadas
    return strike
def Consultas_opção_tipo(symbol):
    header = {"Access-Token": Token}
    dados = requests.get('https://api.oplab.com.br/v3/market/options/details/{}'.format(symbol),headers=header).json()
    tipo=dados['category']
    # df=pd.DataFrame((dados),columns=colunas_desejadas)
# Criar um novo dicionário contendo apenas as colunas desejadas
    return tipo