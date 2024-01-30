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

tabela = tabela.query(f"(moneyness=='ATM')  & category=='CALL' & due_date =='2024-02-16' ")
print(tabela[['symbol','due_date','Volatilidade Implicita(ask)','Volatilidade Implicita(bid)','ask','bid','Preco_ativo','strike']])


