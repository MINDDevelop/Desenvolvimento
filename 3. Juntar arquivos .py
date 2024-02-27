import pandas as pd
import Functions as tt 
import cacluldora_BS as BS 
from datetime import datetime,timedelta
import pandas as pd
import numpy as np
import os
from openpyxl import load_workbook

Hoje=datetime.today().strftime('%Y_%m_%d')
caminho1=r'\\Server\backup usuarios\Base De dados\Base de dados Com vols'
caminho2=r'\\Server\backup usuarios\Base De dados\Base de dados Sem Vols'
df1=pd.read_excel(rf'{caminho1}\Planilha_com_vol_{Hoje}.xlsx')
df2=pd.read_excel(rf'{caminho2}\Planilha_sem_vol_{Hoje}.xlsx')
df_merded = pd.concat([df1, df2],ignore_index=True)
df_merded.drop(columns=['Unnamed: 0'], inplace=True)


caminho_salvar=r'C:\Users\vgonçalves\Desktop\Desenvolvimento\Desenvolvimento\Arquivos\Base de dados completa'
df_merded.to_excel(rf'{caminho_salvar}\Base_de_dados_{Hoje}.xlsx')