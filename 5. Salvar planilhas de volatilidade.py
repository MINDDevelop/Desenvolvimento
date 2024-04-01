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
vols_atm.to_excel(rf'{caminho_salvar}\Base_de_dados_Volatilidade_{Hoje}.xlsx',index=False)
