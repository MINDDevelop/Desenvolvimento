import Teste as tt 
import cacluldora_BS as BS 
from datetime import datetime,timedelta

import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import statistics as st
import numpy as np
import arch

###############################################################################################
#                            Buscar o Token da API                                            #  
###############################################################################################
pd.set_option('display.width', 10000)
email='victor.drone2013@gmail.com'
senha='899513Vi!'
Token=tt.get_token(email,senha)
###############################################################################################
#                              selecionar o Ticker                                            #  
###############################################################################################

Ticker= input("Digite o Ticker desejado: ")

###############################################################################################
#                            Selecionar as opções ativas                                      #  
###############################################################################################

tabela=tt.opcoes_ativos(Token,Ticker)

###############################################################################################
#                            Calcular a vol implicita                                         #  
###############################################################################################
tabela['Preco_ativo']=tt.Cotacoes(Token,Ticker)
L_ask=tabela.apply(BS.calcular_IV_linha_ask, axis=1)
L_bid=tabela.apply(BS.calcular_IV_linha_bid, axis=1)
tabela.loc[:, 'Volatilidade Implicita(ask)']= L_ask
tabela.loc[:, 'Volatilidade Implicita(bid)']= L_bid
vencimentos=tabela['due_date'].unique()
# print(tabela)

df_vols = pd.DataFrame(columns=['Data do Strike', 'Volatilidade Implicita(ask)', 'Volatilidade Implicita(bid)','DP ask','DP Bid'])
for i in vencimentos:
    tabela_filtrada = tabela.query(f"(category == 'CALL') & (due_date == '{i}') & (volume > 10000) & (moneyness == 'ATM')")
    med_ask_c = tabela_filtrada['Volatilidade Implicita(ask)'].mean()
    med_bid_c = tabela_filtrada['Volatilidade Implicita(bid)'].mean()
    dp_ask_c = tabela_filtrada['Volatilidade Implicita(ask)'].std()
    dp_bid_c = tabela_filtrada['Volatilidade Implicita(bid)'].std()
    
    
    
    df_vols.loc[len(df_vols)] = [i, med_ask_c, med_bid_c,dp_ask_c,dp_bid_c]
df_vols['Data do Strike'] = pd.to_datetime(df_vols['Data do Strike'])
# for i in range(len(df_vols)):
#     if i > 2:  # A partir da terceira linha
#         df_vols.iloc[i, 1:] = df_vols.iloc[i-2:i+1, 1:].mean()
df_teste=df_vols.head(1)
log_media_vol=df_vols['Volatilidade Implicita(ask)'].values[0]
log_desvio_vol=df_vols['DP ask'].values[0]
tempo=1
simulacoes = 10000
resultados = np.empty((simulacoes, tempo))

for s in range(simulacoes):
    random_returns = 1 + np.random.normal(loc=log_media_vol, scale=log_desvio_vol, size=tempo)
print(random_returns.mean())
print(df_vols)
    


