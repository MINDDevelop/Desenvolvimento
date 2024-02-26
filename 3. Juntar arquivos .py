import pandas as pd
import Functions as tt 
import cacluldora_BS as BS 
from datetime import datetime,timedelta
import pandas as pd
import numpy as np
import os
from openpyxl import load_workbook

Hoje=datetime.today().strftime('%Y_%m_%d')
caminho=r'C:\Users\vgonçalves\Desktop\Desenvolvimento\Desenvolvimento\Arquivos'
df1=pd.read_excel(rf'{caminho}\Planilha_com_vol_{Hoje}.xlsx')
df2=pd.read_excel(rf'{caminho}\Planilha_sem_vol_{Hoje}.xlsx')
df_merded = pd.concat([df1, df2],ignore_index=True)
df_merded.drop(columns=['Unnamed: 0'], inplace=True)

df_merded['days_to_maturity']=df_merded.apply(BS.calcular_du,axis=1)
df_merded.to_excel(rf'{caminho}\Base_de_dados_{Hoje}.xlsx')