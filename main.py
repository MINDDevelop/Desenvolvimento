import Functions as tt 
import cacluldora_BS as BS 
from datetime import datetime,timedelta
from scipy.interpolate import interp1d
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt

import statistics as st
import numpy as np

import requests
import numpy as np
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
# email='victor.drone2013@gmail.com'
# senha='899513Vi!'
# Token=tt.get_token(email,senha)
###############################################################################################
#                              selecionar o Ticker                                            #  
###############################################################################################

# Ticker= input("Digite o Ticker desejado:")
print(tt.opcoes_ativos("TASA4"))
###############################################################################################
#                            Selecionar as opções ativas                                      #  
###############################################################################################


###############################################################################################
#                            Calcular a vol implicita                                         #  
###############################################################################################
# tabela['Preco_ativo']=tt.Cotacoes(Token,Ticker)
# L_ask=tabela.apply(BS.calcular_IV_linha_ask, axis=1)
# L_bid=tabela.apply(BS.calcular_IV_linha_bid, axis=1)
# tabela.loc[:, 'Volatilidade Implicita(ask)']= L_ask
# tabela.loc[:, 'Volatilidade Implicita(bid)']= L_bid
# op_atm=tabela.query(f"(moneyness=='ATM')  & category=='CALL' & due_date >'2024-02-16'")

# op_atm=op_atm.rename(columns={
#     'Volatilidade Implicita(ask)': 'VI_ask',
#     'Volatilidade Implicita(bid)': 'VI_bid',
#     'days_to_maturity':'Venc.'
# })
# op_atm = op_atm[~op_atm['symbol'].str.contains('W\d+$', na=False)]
# op_atm['Dif.Book']=(op_atm['ask']-op_atm['bid'])
# op_atm = op_atm[op_atm['Dif.Book'].notna()]
# op_atm=op_atm.query('`Dif.Book`< 0.2 & `Dif.Book`> 0'  )
# op_atm_media_venc=op_atm.groupby('due_date').agg({
#     'VI_ask': 'mean',
#     'VI_bid': 'mean'
# })
# print(op_atm_media_venc)

###############################################################################################
#                            Calcular curvas de vol                                           #  
###############################################################################################
# tabela['Preco_ativo']=tt.Cotacoes(Token,Ticker)
# L_ask=tabela.apply(BS.calcular_IV_linha_ask, axis=1)
# L_bid=tabela.apply(BS.calcular_IV_linha_bid, axis=1)
# tabela.loc[:, 'Volatilidade Implicita(ask)']= L_ask
# tabela.loc[:, 'Volatilidade Implicita(bid)']= L_bid
# op_atm=tabela.query(f"(moneyness=='ATM')  & category=='CALL'")
# op_atm = op_atm[~op_atm['symbol'].str.contains('W\d+$', na=False)]
# op_atm['Dif.Book']=(op_atm['ask']-op_atm['bid'])
# op_atm=op_atm.rename(columns={
#     'Volatilidade Implicita(ask)': 'VI_ask',
#     'Volatilidade Implicita(bid)': 'VI_bid',
#     'days_to_maturity':'Venc.'})
# op_atm=op_atm.query('`Dif.Book`< 0.2 & `Dif.Book`> 0')
# vencimentos=op_atm['due_date'].unique()

# for i in vencimentos:
#     tabela_filtrado=op_atm.query(rf"category == 'CALL' & due_date == '{i}' & moneyness =='ATM'")
#     plt.plot(tabela_filtrado['strike'],tabela_filtrado['VI_ask'],label=f'{i}')
# plt.xlabel("Strike")
# plt.ylabel("Vol.Média")
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
# plt.title("Curvas de Volatilidade para Diferentes Vencimentos")
# plt.grid(True)
# plt.show()
###############################################################################################
#                            entrada de strike e saida de vol                                 #  
###############################################################################################
# tabela['Preco_ativo']=tt.Cotacoes(Token,Ticker)
# L_ask=tabela.apply(BS.calcular_IV_linha_ask, axis=1)
# L_bid=tabela.apply(BS.calcular_IV_linha_bid, axis=1)
# tabela.loc[:, 'Volatilidade Implicita(ask)']= L_ask
# tabela.loc[:, 'Volatilidade Implicita(bid)']= L_bid
# op_atm=tabela.query(f"(moneyness=='ATM')  & category=='CALL'")
# op_atm = op_atm[~op_atm['symbol'].str.contains('W\d+$', na=False)]
# op_atm['Dif.Book']=(op_atm['ask']-op_atm['bid'])
# op_atm=op_atm.rename(columns={
#     'Volatilidade Implicita(ask)': 'VI_ask',
#     'Volatilidade Implicita(bid)': 'VI_bid',
#     'days_to_maturity':'Venc.'})
# op_atm=op_atm.query('`Dif.Book`< 0.2 & `Dif.Book`> 0')
# vencimentos=op_atm['due_date'].unique()
###############################################################################################
#                            calcular volatilidade do ativo dos ultimos 30 dias                                 #  
#############################################################################################
# d1=(datetime.today())
# d2 = d1- timedelta(days=365)
# d1=d1.strftime('%Y-%m-%d')
# d2=d2.strftime('%Y-%m-%d')
# historical_data=tt.cotacao_historica(Token,'PETR4',d2,d1,"1d")
# data = historical_data['data']

# # Cria um DataFrame do pandas
# df = pd.DataFrame(data)

# # Converte a coluna 'time' para o formato de data
# df['time'] = pd.to_datetime(df['time'], unit='ms')
# df['retorno_diario_low'] = df['low'].pct_change()
# df['retorno_diario_high'] = df['high'].pct_change()
# df['retorno_diario_close'] = df['close'].pct_change()
# df['desvio.retorno.close']=df['retorno_diario_close'].rolling(window=3).std()*np.sqrt(252)
# df['desvio.retorno.low']=df['retorno_diario_low'].rolling(window=3).std()*np.sqrt(252)
# df['desvio.retorno.high']=df['retorno_diario_high'].rolling(window=3).std()*np.sqrt(252)
# # print(df[['time','close','retorno_diario_close','desvio.retorno']])


# plt.plot(df['time'].head(10),df['desvio.retorno.low'].head(10))
# plt.plot(df['time'].head(10),df['desvio.retorno.high'].head(10))
# plt.show()

###############################################################################################
#                            Calcular as vols de uma cesta de açõe                            #  
###############################################################################################






# cesta=['PETR4','BOVA11','SMAL11',
# 'VALE3','BOVA11','ELET3','RENT3',
# 'AESB3','MGLU3','WEGE3','BBAS3']

# for acoes in cesta:
#     print(acoes)
#     hoje=datetime.today()
#     hoje=hoje.strftime('%Y_%m_%d')
#     op_dia=tt.opcoes_ativos(acoes)
#     op_dia['Preco_ativo']=tt.Cotacoes(acoes)
#     op_filtered = op_dia
    
#     op_fil=op_filtered.dropna(subset=['last_trade_at'])
#     L_ask=op_fil.apply(BS.calcular_IV_linha_ask, axis=1)
#     L_bid=op_fil.apply(BS.calcular_IV_linha_bid, axis=1)
#     op_fil.loc[:, 'Volatilidade Implicita(ask)']= L_ask
#     op_fil.loc[:, 'Volatilidade Implicita(bid)']= L_bid
#     op_fil['Dif.Book']=(op_fil['ask']-op_fil['bid'])
#     op_fil=op_fil[['symbol','category','strike','Preco_ativo','Volatilidade Implicita(ask)','Volatilidade Implicita(bid)','due_date','Dif.Book','bid','ask',]]
#     op_fil = op_fil[~op_fil['symbol'].str.contains('W\d+$', na=False)]
#     opcoes_call = op_fil[op_fil['category'] == 'CALL']
#     opcoes_call=opcoes_call.rename(columns={
#         'Volatilidade Implicita(ask)': 'VI_ask',
#         'Volatilidade Implicita(bid)': 'VI_bid',
#         'financial_volume':'Volu.',
#         'due_date':'Venc.'})
#     print(opcoes_call)
#     opcoes_call['p.strike'] = (( opcoes_call['Preco_ativo']- opcoes_call['strike'])/opcoes_call['Preco_ativo'])*100
#     opcoes_call['p.strike'] = abs(opcoes_call['p.strike'])
#     opcoes_call['tmoney'] = opcoes_call.apply(tt.determinar_tmoney, axis=1)
#     opcoes_call['tmoney'] = opcoes_call.apply(tt.determinar_tmoney2, axis=1)
#     opcoes_call['in/on'] = opcoes_call.apply(tt.determinar_tmoney, axis=1)
#     opcoes_call.sort_values(by=['tmoney'],ascending=True)
#     opcoes_call = opcoes_call.query("tmoney=='ATM'" )
#     opcoes_call=opcoes_call.sort_values(by=['in/on','p.strike'],ascending=True) 
#     opcoes_put = op_fil[op_fil['category'] == 'PUT']
#     opcoes_put=opcoes_put.rename(columns={
#         'Volatilidade Implicita(ask)': 'VI_ask',
#         'Volatilidade Implicita(bid)': 'VI_bid',
#         'due_date':'Venc.'})
#     opcoes_put['p.strike'] = (( opcoes_put['Preco_ativo']- opcoes_put['strike'])/opcoes_put['Preco_ativo'])*100
#     opcoes_put['p.strike'] = abs(opcoes_put['p.strike'])
#     opcoes_put['tmoney'] = opcoes_put.apply(tt.determinar_tmoney2, axis=1)
#     opcoes_put['in/on'] = opcoes_call.apply(tt.determinar_tmoney, axis=1)
#     opcoes_put.sort_values(by=['tmoney'],ascending=True)
#     opcoes_put = opcoes_put.query("tmoney=='ATM'" )
#     opcoes_put=opcoes_put.sort_values(by=['p.strike'],ascending=True)
    

    
            
#     # print(opcoes_call)
#     with pd.ExcelWriter(f'{acoes}_{hoje}.xlsx', engine='xlsxwriter') as writer:
#     # Salvar cada DataFrame em uma planilha separada
#         opcoes_call.to_excel(writer, sheet_name='CALL', index=False)
#         opcoes_put.to_excel(writer, sheet_name='PUT', index=False)
        

    
    
    
    
