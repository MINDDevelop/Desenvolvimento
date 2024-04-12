import Functions as tt 
import cacluldora_BS as BS 
from datetime import datetime
import pandas as pd
from openpyxl import load_workbook
import io
# from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
caminho=r'\\Server\backup usuarios\Base De dados\Base de dados Com vols'


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
        all_options=pd.concat([all_options,df])
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
tabela['Max_dif_book']=0.01*tabela['close']
tabela=tabela.query("tmoney == 'ATM' and `Dif.Book` <= Max_dif_book and (bid>0 and ask>0) ")
tabela=tabela.reset_index(drop=True)
tabela['VI_bid']=tabela.apply(BS.calcular_IV_hist_bid, axis=1)
tabela['VI_ask']=tabela.apply(BS.calcular_IV_hist_ask, axis=1)
tabela['days_to_maturity']=tabela.apply(BS.calcular_du,axis=1)
tabela['delta_bid']=tabela.apply(BS.calcular_delta_Bid, axis=1)
tabela['delta_ask']=tabela.apply(BS.calcular_delta_Ask, axis=1)
tabela['in/on']=tabela.apply(tt.determinar_tmoney,axis=1)
atm_com_book=tabela
print('Salvando base no excel')
atm_com_book.to_excel(rf'{caminho}\Planilha_com_vol_{Hoje}.xlsx')

