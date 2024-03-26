import datetime
import pandas as pd
import Functions as tt
import re
import numpy as np
import cacluldora_BS as bs
import datetime

Base_vols=pd.read_excel(r"\\Server\backup usuarios\Base De dados\Base de dados Volatilidade\Base_de_dados_Volatilidade_2024_03_26.xlsx")

Base_vols=Base_vols.groupby(['ativo_alvo','due_date','category'],as_index=False).agg({
    'VI_bid': 'mean',
    'VI_ask': 'mean'
},axis=0)
caminho= r"C:\Users\vgonçalves\Downloads\Negócios em destaques - 25.03.2024.xlsx"
data_atual ='2024-03-25' #datetime.date.today()
df=pd.read_excel(caminho)
df['Hora'] = data_atual + ' ' + df['Hora'].astype(str)
df['ativo_alvo'] = df['Ativo'].apply(tt.Consultas_ativoalvo_opcao)
df['Cotacao']=df.apply(lambda row: tt.Cotação_historica(row['ativo_alvo'], row['Hora'], row['Hora']), axis=1)
df['category']=df['Ativo'].apply(tt.Consultas_opção_tipo)
df['strike']=df['Ativo'].apply(tt.Consultas_opção_strike)
df['due_date']=df['Ativo'].apply(tt.Consultas_opção_venc)
merged_df= pd.merge(Base_vols,df, on=['ativo_alvo','category','due_date'],how='inner')
merged_df=merged_df[['Hora','Qtde','Volume','Comprador','Vendedor','ativo_alvo','Ativo','Cotacao','strike','category','VI_bid','VI_ask','Preço','due_date']]
merged_df['Vol_media']=merged_df[['VI_bid', 'VI_ask']].mean(axis=1)
merged_df=merged_df[['Hora','Qtde','Volume','Comprador','Vendedor',
       'ativo_alvo','Ativo','Cotacao','strike','category',
       'Vol_media','Preço','due_date']]
merged_df['dias']= merged_df.apply(bs.calcular_du,axis=1)
merged_df['dias']=merged_df['dias']/252
merged_df['juros']=0.1075
merged_df['pricer mind']=merged_df.apply(lambda row: bs.black_scholes_option_price(row['Vol_media'], row['Cotacao'], row['strike'],row['dias'],row['juros'],row['category']), axis=1)
merged_df=merged_df[['Hora','Qtde','Volume','Comprador','Vendedor','ativo_alvo','Ativo','Vol_media','Preço','pricer mind']]
merged_df.to_excel('Negócios em destaques - 25.03.2024.xlsx')