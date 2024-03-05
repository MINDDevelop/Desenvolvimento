import Functions as tt 
import cacluldora_BS as BS 
from datetime import datetime
import pandas as pd
from openpyxl import load_workbook
import io
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
caminho=r'\\Server\backup usuarios\Base De dados\Base de dados Com vols'


pd.set_option('display.width', 10000)
Acoes=tt.acoes_options()
Acoes_op=Acoes['symbol'].unique()
price=pd.DataFrame(tt.acoes_options())
price=price.rename(columns={
     'symbol':'ativo_alvo'})
all_options=pd.DataFrame(columns=['symbol','category','strike','ask','bid','due_date','ativo_alvo'])
for ativos in Acoes_op:
    print('fazendo com o ticker',ativos)
    try:
        tabela=tt.opcoes_ativos(ativos)
        tabela=pd.DataFrame(tabela)
        tabela['ativo_alvo']=ativos
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
calcular_vols=tabela
calcular_vols['p.strike'] = ((calcular_vols['close']- calcular_vols['strike'])/calcular_vols['close'])*100
calcular_vols['p.strike'] = abs(calcular_vols['p.strike'])
calcular_vols['tmoney'] = calcular_vols.apply(tt.determinar_tmoney3,axis=1)
calcular_vols['Max_dif_book']=0.01*calcular_vols['close']
calcular_vols=calcular_vols.query("tmoney == 'ATM' and `Dif.Book` <= Max_dif_book and (bid>0 and ask>0) ")
calcular_vols=calcular_vols.reset_index(drop=True)
calcular_vols['VI_bid']=calcular_vols.apply(BS.calcular_IV_hist_bid, axis=1)
calcular_vols['VI_ask']=calcular_vols.apply(BS.calcular_IV_hist_ask, axis=1)
calcular_vols['days_to_maturity']=calcular_vols.apply(BS.calcular_du,axis=1)
calcular_vols['delta_bid']=calcular_vols.apply(BS.calcular_delta_Bid, axis=1)
calcular_vols['delta_ask']=calcular_vols.apply(BS.calcular_delta_Ask, axis=1)
calcular_vols['in/on']=calcular_vols.apply(tt.determinar_tmoney,axis=1)

atm_com_book=calcular_vols
print('Salvando base no excel')
atm_com_book.to_excel(rf'{caminho}\Planilha_com_vol_{Hoje}.xlsx')
atm_com_book['Data_registro']= datetime.today().strftime('%Y-%m-%d')
print('salvando base na azzure')
connect_str = 'DefaultEndpointsProtocol=https;AccountName=dbmindvolatilidade;AccountKey=VAdYwii7EfjX0WQpnDov9iHBdZVcYMyfxyZ1vKn8cRVPToI3/Mt45UVEpy76fJqxYST9vB6DZaQz+AStQKDbQQ==;EndpointSuffix=core.windows.net'
container_name = 'vols-atm'
blob_name = f'Planilha_com_vol_{Hoje}.csv'
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
output = io.StringIO()
atm_com_book.to_csv(output,index=False)
output.seek(0)
blob_client.upload_blob(output.getvalue(), overwrite=True)