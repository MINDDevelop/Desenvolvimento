import Functions as tt 
import cacluldora_BS as BS 
from datetime import datetime
import pandas as pd
from openpyxl import load_workbook
caminho=r'C:\Users\victo\MIND\Desenvolvimento\Arquivos'


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
atm_com_book.to_csv(rf'{caminho}\Planilha_com_vol_{Hoje}.csv')