import Functions as tt 
import cacluldora_BS as BS 
from datetime import datetime
import pandas as pd
from openpyxl import load_workbook
import io
# from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
caminho=r'\\WIN-RJAPD707RCN\Arquivos_bulk\Base de dados Com vols'


pd.set_option('display.width', 10000)
Acoes=tt.acoes_options()
Acoes_op=Acoes['symbol'].unique()
Acoes_op = [codigo for codigo in Acoes_op if codigo != 'PCAR99']

price=pd.DataFrame(tt.acoes_options())
price=price.rename(columns={
     'symbol':'ativo_alvo'})
all_options=pd.DataFrame(columns=['symbol','category','strike','ask','bid','due_date','ativo_alvo'])
for ativos in Acoes_op:
    print('fazendo com o ticker',ativos)
    try:
        tabela=tt.opcoes_ativos(ativos)
        tabela=pd.DataFrame(tabela)
        tabela['ativo_alvo']=str(ativos)
        
        df=pd.merge(tabela,price,on='ativo_alvo',how='inner')
        all_options=pd.concat([all_options,df]) #'ITSAR107'
    except:
        print('Problema com a ação de ticker:',ativos)

print('Historico concluido com sucesso')
Hoje=datetime.today().strftime('%Y_%m_%d')
tabela=all_options
tabela = tabela[~tabela['symbol'].str.contains('W\d+$', na=False)]
tabela['Dif.Book']=(tabela['ask']-tabela['bid'])
tabela=tabela.reset_index(drop=True)


tabela['p.strike'] = ((tabela['close']- tabela['strike'])/tabela['close'])*100
tabela['p.strike'] = abs(tabela['p.strike'])
tabela['tmoney'] = tabela.apply(tt.determinar_tmoney3,axis=1)

tabela=tabela.query("tmoney == 'ATM' and `Dif.Book` <= 0.2 and (bid>0 and ask>0) ")
tabela=tabela.reset_index(drop=True)
tabela['VI_bid']=tabela.apply(BS.calcular_IV_hist_bid, axis=1)
tabela['VI_ask']=tabela.apply(BS.calcular_IV_hist_ask, axis=1)
tabela['days_to_maturity']=tabela.apply(BS.calcular_du,axis=1)
tabela['delta_bid']=tabela.apply(BS.calcular_delta_Bid, axis=1)
tabela['delta_ask']=tabela.apply(BS.calcular_delta_Ask, axis=1)
tabela['in/on']=tabela.apply(tt.determinar_tmoney,axis=1)
tabela['data']=datetime.today().strftime('%Y-%m-%d')
atm_com_book=tabela[['data','ativo_alvo','symbol','category','strike','close','due_date',
                     'days_to_maturity','tmoney','in/on','bid','ask','VI_bid','VI_ask',
                     'delta_bid','delta_ask']]
print('Salvando base no csv')
atm_com_book.to_csv(rf'{caminho}\Planilha_com_vol_{Hoje}.csv',index=False)

