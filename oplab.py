import Teste as tt 
import cacluldora_BS as BS 
from datetime import datetime,timedelta
import requests
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

pd.set_option('display.width', 10000)
email='victor.drone2013@gmail.com'
senha='899513Vi!'
Token=tt.get_token(email,senha)
Ticker= input("Digite o Ticker desejado: ")
tabela=tt.opcoes_ativos(Token,Ticker) 
tabela['Preco_ativo']=tt.Cotacoes(Token,Ticker)
L_ask=tabela.apply(BS.calcular_IV_linha_ask, axis=1)
L_bid=tabela.apply(BS.calcular_IV_linha_bid, axis=1)
tabela.loc[:, 'Volatilidade Implicita(ask)']= L_ask
tabela.loc[:, 'Volatilidade Implicita(bid)']= L_bid
vencimentos=tabela['due_date'].unique()

for i in vencimentos:
    tabela_filtrado=tabela.query(rf"category == 'CALL' & due_date == '{i}' & volume > 100 & moneyness =='ATM'")
    tabela_filtrado.to_csv(rf'{Ticker}_{i}.csv')