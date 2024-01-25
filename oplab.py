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
tabela=tt.opcoes_ativos(Token,'PETR4')
tabela['Preco_ativo']=tt.Cotacoes(Token,'PETR4')
tabela_filtrado=tabela
resultados = tabela_filtrado.apply(BS.calcular_IV_linha_ask, axis=1)
resultados2 = tabela_filtrado.apply(BS.calcular_IV_linha_bid, axis=1)
tabela_filtrado.loc[:, 'Volatilidade Implicita(ask)'] = resultados
tabela_filtrado.loc[:, 'Volatilidade Implicita(bid)'] = resultados2
tabela_filtrado_16=tabela_filtrado.query("category == 'CALL' & days_to_maturity == 16 & volume > 10000 & moneyness =='ATM'")
tabela_filtrado_36=tabela_filtrado.query("category == 'CALL' & days_to_maturity == 60 & volume > 10000 & moneyness =='ATM'")
# tabela_filtrado_16[['symbol','Volatilidade Implicita(ask)','Volatilidade Implicita(bid)']].to_csv('Vol_PETR4_16du_PUT.csv',sep=';')
# tabela_filtrado_36[['symbol','Volatilidade Implicita(ask)','Volatilidade Implicita(bid)']].to_csv('Vol_PETR4_36du_PUT.csv',sep=';')
print(tabela_filtrado_36)

# plt.plot(tabela_filtrado_16['strike'], tabela_filtrado_16['volatility'], label='Volatilidade Implicita 16du', color='blue')
# plt.plot(tabela_filtrado_36['strike'], tabela_filtrado_36['volatility'], label='Volatilidade Implicita 36du', color='red')
# plt.xlabel('Strike')
# plt.ylabel('Volatilidade Implicita')
# plt.title('Gráfico Comparativo')
# plt.legend()
# plt.show()