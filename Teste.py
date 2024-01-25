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

style.use('dark_background')
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


### FUNÇÃO PARA RETORNAR A SÉRIE HISTÓRICA
def getFechamentosPorData(token,symbol,data_inicio,data_fim,resolution="1d"):     
    ## HEADER DE AUTENTICAÇÃO
    header = {"Access-Token": token}
    
    ## CHAMADA NA API 
    dados = requests.get('https://api.oplab.com.br/v3/market/historical/{}/{}?from={}&to={}?smooth=true'.format(
    symbol, resolution, data_inicio.strftime("%Y%m%d%H%M"), data_fim.strftime("%Y%m%d%H%M")),
                        headers=header).json()['data']
    ## CONSTRUÇÃO DO DATAFRAME NO PANDAS
    fechamentos = []
    datas_list = []
    for i in dados:
        fechamentos.append(i['close'])
        datas_list.append(datetime.fromtimestamp(int(str(i['time'])[:10])))
    df = pd.DataFrame({'Close': fechamentos}, index = datas_list)
    return df

### FUNÇÃO PARA CALCULR A FUNÇÃO POLINOMIAL DA GRADE DO DIA REQUISITADO
def smile_do_dia(token,symbol,data_estudo,spot_price,lista_strikes,vctos = 1,range_moneyness=(0.10,1.8),graus_polin=3,call_put = 'PUT'):
    if isinstance(lista_strikes,list) == 0:
        print('Strikes deveria ser lista!')
        lista_strikes = []
    calculou = 0
    contador = 0
    while calculou == 0:
        contador += 1
        if contador > 5:
            break
        print(data_estudo)
        c = requests.get(
            'https://api.oplab.com.br/v3/market/historical/options/{}/{}/{}'.format(symbol, data_estudo.date(), data_estudo.date()),
            headers={"Access-Token": token}).json()
        lista_vcto_atual = []
        w = []
        strikes = []
        vols = []
        x = 0
        y = 0
        polynomio_list = []
        if len(c) < 5:
            data_estudo = data_estudo + timedelta(days=1)
            continue
        for i in c:
            moneyness = i['strike'] / i['spot']['price']
            mes_vcto = datetime.strptime(i['due_date'][:10], "%Y-%m-%d").month
            ano_vcto = datetime.strptime(i['due_date'][:10], "%Y-%m-%d").year
            maturity = (datetime.strptime(i['due_date'][:10], "%Y-%m-%d") - datetime.strptime(i['time'][:10], "%Y-%m-%d")).days
            if mes_vcto == (data_estudo.month+vctos) and ano_vcto == data_estudo.year and maturity > 10 and i['type'] == call_put and moneyness > range_moneyness[0] and moneyness < range_moneyness[1]:
                lista_vcto_atual.append(i)
        if len(lista_vcto_atual) < 3:
            data_estudo = data_estudo + timedelta(days=1)
            continue
        for j in lista_vcto_atual:
            strikes.append(j['strike'] / j['spot']['price'])
            vols.append(j['volatility'])
        if len(strikes) == 0 or len(vols) == 0:
            data_estudo = data_estudo + timedelta(days=1)
            continue
        df = pd.DataFrame({'s':strikes,'v':vols})
        df = df.sort_values(by = 's')
        x = list(df['s'])
        y = list(df['v'])
        if len(x) == 0 or len(y) == 0:
            data_estudo = data_estudo - timedelta(days=1)
            continue
        if len(x) > 0 and len(y) > 0:
            calculou = 1
            z = np.polyfit(x, y,graus_polin)
            polynomio_list = []
            for i in x:
                polynomio_list.append(np.poly1d(z)(i))
            if len(lista_strikes) == 0:
                continue
            else:
                for jj in lista_strikes:
                    mnnss = jj / spot_price
                    w.append(np.poly1d(z)(mnnss))
    return (polynomio_list,x,y,w)

### INSERIR EMAIL E SENHA --> get_token('seu@email.com','sua_senha')
# try:
#     token = get_token('victor.drone2013@gmail.com','899513Vi!')
# except:
#     print('TOKEN ERRADO')
#     exit()

# ### DATA INICIAL DO ESTUDO
# data_inicial = datetime(2022,9,25)

# ### NÚMERO DE DIAS APÓS A DATA INICIAL QUE DEVERÁ SER CALCULADA A SMILE
# dias_sequencia = 10

# datas = [x for x in range(dias_sequencia)]

# ### INDICAR ATIVO E O TIPO DE OPÇÃO (CALL OU PUT)
# symbol = 'PETR4'
# tipo = 'PUT'

# ### 'C:/sua_pasta/
# folder_adress = r'C:\Users\vgonçalves\Desktop\Desenvolvimento\ ' 
# if folder_adress == '':
#     print('INDICAR PASTA')
#     exit()

# ### GERAR IMAGENS
# file_list = []
# for i in datas:
#     data_estudo = data_inicial + timedelta(days=i)
#     vctos = 1
#     spot_price = getFechamentosPorData(token,symbol,data_estudo,data_estudo)
#     if len(spot_price['Close']) > 0:
#         chamada_api = smile_do_dia(token,symbol,data_estudo,spot_price['Close'][0],[30],vctos,(0.70,1.10),3,tipo)
#     else:
#         chamada_api = []
    
#     if len(chamada_api)>0:
#         print(chamada_api[3])
#         fig, ax1 = plt.subplots(1, 1, figsize = (20,12))
#         x = chamada_api[1]
#         y = chamada_api[0]
#         ax1.plot(x,y, color = 'green', linewidth = 7)
#         ax1.set_xlabel('Moneyness',size = 20)
#         ax1.set_ylabel('Vol Implícita %',size = 20)
#         ax1.set_title('Vol Implícita X Moneyness {} {}'.format(symbol,data_estudo.date()),size = 20)
#         for j in range(3):
#             plt.savefig(folder_adress+str(i)+str(j)+'.png')
#             file_list.append('{}{}.png'.format(i,j))
#         plt.close()
#     else:
#         continue

# ### GERAR GIF
# with imageio.get_writer(folder_adress+'mygif.gif', mode='I') as writer:
#     for filename in file_list:
#         image = imageio.imread(folder_adress+filename)
#         writer.append_data(image)

# ### DELETAR IMAGENS
# for filename in set(file_list):
#     os.remove(folder_adress+filename)

def opcoes_ativos(Token,symbol):
    header = {"Access-Token": Token}
    data_atual=datetime.today()
    data_inicio= (datetime.today()- timedelta(days=1))
    data_fim = data_atual
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
    df_filtrado=df[['symbol','category','days_to_maturity','strike','close','ask','bid']]
    dados = requests.get('https://api.oplab.com.br/v3/market/historical/options/{}/{}/{}'.format(symbol, data_inicio.strftime("%Y%m%d%H%M"), data_fim.strftime("%Y%m%d%H%M")),
                    headers=header).json()
    df_moneyness=pd.DataFrame(dados)
    df_moneyness = df_moneyness[['symbol','moneyness','volatility']]
    df_final = pd.merge(df_filtrado, df_moneyness, on='symbol')
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

