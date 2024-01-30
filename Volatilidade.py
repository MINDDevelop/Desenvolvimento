import Teste as tt 
import cacluldora_BS as BS 
from datetime import datetime,timedelta
import requests
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from scipy import interpolate
import numpy as np
from scipy.interpolate import CubicSpline

pd.set_option('display.width', 10000)
email='victor.drone2013@gmail.com'
senha='899513Vi!'
Token=tt.get_token(email,senha)
###############################################################################################
#                              selecionar o Ticker                                            #  
###############################################################################################

Ticker='PETR4'

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
tabela = tabela.query(f"(moneyness=='ATM')  & category=='CALL' & days_to_maturity <= 90 & volume > 100 ")
print(tabela[['symbol','due_date','Volatilidade Implicita(ask)','Volatilidade Implicita(bid)'
              ,'ask','bid','Preco_ativo','strike']])




tabela_filtrado = tabela.query(rf"category == 'CALL' & due_date == '2024-02-16' & volume > 100 & moneyness =='ATM'")

if not tabela_filtrado.empty:
    tabela_filtrado.loc[:, "volatility_implicita_media_ask"] = tabela_filtrado.groupby("strike")["Volatilidade Implicita(ask)"].transform("mean")
    tabela_filtrado.loc[:, "volatility_implicita_media_bid"] = tabela_filtrado.groupby("strike")["Volatilidade Implicita(bid)"].transform("mean")
    tabela_filtrado.sort_values(by="strike", inplace=True)
    
    for vencimento, grupo_vencimento in tabela_filtrado.groupby('due_date'):
        plt.plot(grupo_vencimento['strike'], grupo_vencimento['volatility_implicita_media_ask'], label=str(vencimento))

# Adicionar rótulos e legendas ao gráfico
plt.figure(figsize=(10, 6))
plt.rcParams['figure.figsize'] = [14, 10]
plt.xlabel("Strike")
plt.ylabel("Volatilidade média")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.title("Curvas de Volatilidade para Diferentes strikes")
plt.grid(True)
plt.show()


