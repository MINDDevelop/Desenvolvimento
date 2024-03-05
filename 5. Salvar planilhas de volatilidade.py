import Functions as tt 
import cacluldora_BS as BS 
from datetime import datetime,timedelta
import pandas as pd
import numpy as np
import os
from openpyxl import load_workbook
import io
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

caminho=r'\\Server\backup usuarios\Base De dados\Base de dados Com vols'
Hoje=datetime.today().strftime('%Y_%m_%d')
vols=pd.read_excel(rf'{caminho}\Planilha_com_vol_{Hoje}.xlsx')
vols['in/on']=vols.apply(tt.determinar_tmoney,axis=1)
vols['VI_ask']=vols['VI_ask']/100
vols['VI_bid']=vols['VI_bid']/100
vols['Dif']=vols['close']* 0.01
vols=vols.query('`Dif.Book`<= Dif ')




vols_atm=vols.groupby(['ativo_alvo','due_date','category','in/on'],as_index=False).agg({
    'VI_bid': 'mean',
    'VI_ask': 'mean'
    
},axis=0)
caminho_salvar = r'\\Server\backup usuarios\Base De dados\Base de dados Volatilidade'
vols_atm.to_excel(rf'{caminho_salvar}\Base_de_dados_Volatilidade_{Hoje}.xlsx')
vols_atm['Data_Registro'] = datetime.today().strftime('%Y-%m-%d')
connect_str = 'DefaultEndpointsProtocol=https;AccountName=dbmindvolatilidade;AccountKey=VAdYwii7EfjX0WQpnDov9iHBdZVcYMyfxyZ1vKn8cRVPToI3/Mt45UVEpy76fJqxYST9vB6DZaQz+AStQKDbQQ==;EndpointSuffix=core.windows.net'
container_name = 'base-dados-volatilidade'
blob_name = f'Base_de_dados_Volatilidade_{Hoje}.csv'
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
output = io.StringIO()
vols_atm.to_csv(output,index=False)
output.seek(0)
blob_client.upload_blob(output.getvalue(), overwrite=True)