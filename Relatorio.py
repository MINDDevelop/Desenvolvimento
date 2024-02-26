import pandas as pd
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import Functions as tt
import cacluldora_BS as BS
pd.set_option('display.width', 1000)

dados= pd.read_excel(r'C:\Users\vgonçalves\Downloads\Relatório 06.02.2024.xlsx',sheet_name='06.02.2024')
dados['ativo_alvo']=dados['Ativo'].apply(tt.Consultas_opção)
dados['strike'] = dados['ativo_alvo'].apply(lambda x: x['strike'])
dados['Venc.'] = dados['ativo_alvo'].apply(lambda x: x['due_date'])
dados['P.A.Alvo'] = dados['ativo_alvo'].apply(lambda x: x['spot_price'])
dados['Tipo'] = dados['ativo_alvo'].apply(lambda x: x['type'])
dados['ativo_alvo'] = dados['ativo_alvo'].apply(lambda x: x['parent_symbol'])
dados.to_csv('Relatiorio.csv')
rel=pd.read_csv(r'C:\Users\vgonçalves\Desktop\Desenvolvimento\Desenvolvimento\Relatiorio.csv')

C_hist = pd.DataFrame(columns=['ativo_alvo', 'Hora', 'spot'])
novo_df = rel.drop(columns=rel.columns[0])
novo_df=novo_df.rename(columns={
     'Preço': 'price',
     'symbol':'ativo_alvo'})
Acoes=novo_df['ativo_alvo'].unique()
for i in Acoes:
    novos=pd.DataFrame(tt.cotacoao(f'{i}'))
    C_hist=pd.concat([novos,C_hist],ignore_index=True)
C_hist=C_hist.drop(columns=['ativo_alvo'])
C_hist=C_hist.rename(columns={
     'Preço':'price',
     'symbol':'ativo_alvo'})
C_hist=C_hist.sort_values('Hora')
novo_df=novo_df.sort_values('Hora')
novo_df['Hora'] = pd.to_datetime(novo_df['Hora'])
C_hist['Hora'] = pd.to_datetime(C_hist['Hora'])
novo_df['Hora']=novo_df['Hora']-timedelta(1) 
novo_df=novo_df.drop(columns=['Volume','Comprador','Vendedor'])
merged_df= pd.merge_asof(novo_df,C_hist,on='Hora',by='ativo_alvo', direction='nearest')
merged_df=merged_df.drop(columns=['P.A.Alvo'])
merged_df['Vol']=merged_df.apply(BS.calcular_IV_nego, axis=1)


# # ###################################################################################################################################

acoes = rel['ativo_alvo'].unique()
acoes=acoes[acoes!='IBOV']
hoje=datetime.today()
hoje=hoje.strftime('%Y_%m_%d')

dfs=pd.DataFrame()
for acoes in acoes:

     try:
          if acoes=='IBOV' :
               pass

          else:
                         
               hoje=datetime.today()
               hoje=hoje.strftime('%Y_%m_%d')
               op_dia=tt.opcoes_ativos(acoes)
               op_dia['Preco_ativo']=tt.Cotacoes(acoes)
               op_filtered = op_dia

               op_fil=op_filtered.dropna(subset=['last_trade_at'])
               L_ask=op_fil.apply(BS.calcular_IV_linha_ask, axis=1)
               L_bid=op_fil.apply(BS.calcular_IV_linha_bid, axis=1)
               op_fil.loc[:, 'Volatilidade Implicita(ask)']= L_ask
               op_fil.loc[:, 'Volatilidade Implicita(bid)']= L_bid
               op_fil['Dif.Book']=(op_fil['ask']-op_fil['bid'])
               op_fil=op_fil[['symbol','category','strike','Preco_ativo','Volatilidade Implicita(ask)','Volatilidade Implicita(bid)','due_date','Dif.Book','bid','ask',]]
               op_fil = op_fil[~op_fil['symbol'].str.contains('W\d+$', na=False)]
               opcoes_call = op_fil
               opcoes_call=opcoes_call.rename(columns={
               'Volatilidade Implicita(ask)': 'VI_ask',
               'Volatilidade Implicita(bid)': 'VI_bid',
               'financial_volume':'Volu.',
               'due_date':'Venc.'})

               opcoes_call['p.strike'] = (( opcoes_call['Preco_ativo']- opcoes_call['strike'])/opcoes_call['Preco_ativo'])*100
               opcoes_call['p.strike'] = abs(opcoes_call['p.strike'])
               opcoes_call['tmoney'] = opcoes_call.apply(tt.determinar_tmoney, axis=1)
               opcoes_call['tmoney'] = opcoes_call.apply(tt.determinar_tmoney2, axis=1)
               opcoes_call['in/on'] = opcoes_call.apply(tt.determinar_tmoney, axis=1)
               opcoes_call.sort_values(by=['tmoney'],ascending=True)
               opcoes_call = opcoes_call.query("tmoney=='ATM'" )
               opcoes_call=opcoes_call.sort_values(by=['in/on','p.strike'],ascending=True)
               dfs=pd.concat([dfs,opcoes_call])
               
          
               print(acoes)
     except:
          print('deu ruim:',acoes)
dfs=dfs.reset_index()

options_calculated=dfs[['symbol','category','strike','VI_ask','VI_bid','tmoney','in/on']] 
df_final=pd.merge(merged_df,options_calculated,left_on='Ativo', right_on='symbol',how='left')
df_fi = df_final[df_final['category'].notna()]
df_fi2=df_final[df_final['category'].isna()]
df_fi2=df_fi2[df_fi2['ativo_alvo']!='IBOV']
df_fi2['Vol']=df_fi2['ativo_alvo'].apply(tt.ewma)
df_fi['Vol']=(df_fi['VI_ask']+df_fi['VI_bid'])/2
df_fi=df_fi.drop(columns=['symbol','category','VI_ask','VI_bid'])
df_fi2=df_fi2.drop(columns=['symbol','category','VI_ask','VI_bid'])
Final=pd.concat([df_fi,df_fi2])
Final['Dias_venc.'] = Final['Venc.'].apply(lambda x: BS.quantidades_du(x, datetime.today().strftime("%Y-%m-%d")))

Final['Pricer'] = Final.apply(lambda row: BS.black_scholes_option_price(row['Vol']/100, row['spot'], row['strike_x'], (row['Dias_venc.'])/252, 0.1125, row['Tipo']), axis=1)
Final=Final[['Ativo','price','Pricer','strike_x','Venc.','Vol','tmoney','Dias_venc.']]
Final.to_excel('Relatorio_final_.xlsx')




     
     


