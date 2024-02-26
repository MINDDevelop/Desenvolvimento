import Functions as tt 
import cacluldora_BS as BS 
from datetime import datetime,timedelta
import pandas as pd
import numpy as np
import os
from openpyxl import load_workbook


caminho=r'C:\Users\vgonçalves\Desktop\Desenvolvimento\Desenvolvimento\Arquivos'

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
calcular_vols=calcular_vols.query("(tmoney == 'ATM' and `Dif.Book` >= Max_dif_book) or (tmoney != 'ATM')")
calcular_vols=calcular_vols.reset_index(drop=True)
atm_com_book=calcular_vols
calcular_vols['days_to_maturity']=calcular_vols.apply(BS.calcular_du,axis=1)
calcular_vols['VI_bid']=''
calcular_vols['VI_ask']=''
calcular_vols['delta_bid']=''
calcular_vols['delta_ask']=''
calcular_vols['in/on']=calcular_vols.apply(tt.determinar_tmoney,axis=1)
atm_com_book.to_excel(rf'{caminho}\Planilha_sem_vol_{Hoje}.xlsx')