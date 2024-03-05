import pandas as pd
import Functions as tt 
import cacluldora_BS as BS 
from datetime import datetime,timedelta
import pandas as pd
import numpy as np
import os
from openpyxl import load_workbook
import io
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

Hoje=datetime.today().strftime('%Y_%m_%d')
caminho1=r'\\Server\backup usuarios\Base De dados\Base de dados Com vols'
caminho2=r'\\Server\backup usuarios\Base De dados\Base de dados Sem Vols'
df1=pd.read_excel(rf'{caminho1}\Planilha_com_vol_{Hoje}.xlsx')
df2=pd.read_excel(rf'{caminho2}\Planilha_sem_vol_{Hoje}.xlsx')
df_merded = pd.concat([df1, df2],ignore_index=True)
df_merded.drop(columns=['Unnamed: 0'], inplace=True)


caminho_salvar=r'\\Server\backup usuarios\Base De dados\Base de dados Completa'
df_merded.to_excel(rf'{caminho_salvar}\Base_de_dados_{Hoje}.xlsx')
df_merded['Data_registro']= datetime.today().strftime('%Y-%m-%d')
connect_str = 'DefaultEndpointsProtocol=https;AccountName=dbmindvolatilidade;AccountKey=VAdYwii7EfjX0WQpnDov9iHBdZVcYMyfxyZ1vKn8cRVPToI3/Mt45UVEpy76fJqxYST9vB6DZaQz+AStQKDbQQ==;EndpointSuffix=core.windows.net'
container_name = 'base-dados-completa'
blob_name = f'Base_de_dados_{Hoje}.csv'
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
output = io.StringIO()
df_merded.to_csv(output,index=False)
output.seek(0)
blob_client.upload_blob(output.getvalue(), overwrite=True)