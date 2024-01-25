import Teste as tt 
import cacluldora_BS as BS 
from datetime import datetime,timedelta
import requests
import pandas as pd
pd.set_option('display.width', 1000)
email='victor.drone2013@gmail.com'
senha='899513Vi!'
Token=tt.get_token(email,senha)
tabela=tt.opcoes_ativos(Token,'PETR4')
tabela['Preco_ativo']=tt.Cotacoes(Token,'PETR4')
condicao = tabela['ask'] > 0

tabela_filtrado=tabela[condicao]

resultados = tabela_filtrado.apply(BS.calcular_IV_linha, axis=1)

tabela_filtrado.loc[:, 'Volatilidade Implicita'] = resultados
tabela_filtrado.loc[:, 'moneyness'] = 'ATM'
tabela_filtrado.loc[:, 'category'] = 'CALL'

tabela_filtrado.loc[:, 'Diferença book'] = (tabela_filtrado['ask'] - tabela_filtrado['bid']).abs()
condicao = tabela_filtrado['Diferença book'] <= 0.5
df_filtrado = tabela_filtrado[condicao]
print(df_filtrado)

#março, diferença bid-ask=0.1