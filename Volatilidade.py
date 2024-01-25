import requests
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings
from datetime import datetime,timedelta
import imageio
import os
from matplotlib import style

def get_token(email,senha):
    ## BODY PARA REQUISIÇÃO NA API
    body = {"email": email,"password": senha}
    
    ## CHAMADA NA API
    r = requests.post('https://api.oplab.com.br/v3/domain/users/authenticate',json=body).json()['access-token']
    return r

def getopppp(token,symbol,data_inicio,data_fim):     
    ## HEADER DE AUTENTICAÇÃO
    header = {"Access-Token": token}
    
    ## CHAMADA NA API 
    dados = requests.get('https://api.oplab.com.br/v3/market/historical/options/{}/{}/{}'.format(
    symbol, data_inicio.strftime("%Y%m%d%H%M"), data_fim.strftime("%Y%m%d%H%M")),
                        headers=header).json()
    df=pd.DataFrame(dados)
    return df

email='victor.drone2013@gmail.com'
senha='899513Vi!'
Token=get_token(email,senha)
data_inicio = datetime(2024, 1, 24)
data_fim = datetime(2024, 1, 24)
print(getopppp(Token,'PETR4',data_inicio,data_fim))

