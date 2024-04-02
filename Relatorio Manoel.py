import pandas as pd

# df=pd.read_excel(r"\\Server\backup usuarios\Base De dados\Base de dados Volatilidade\Base_de_dados_Volatilidade_2024_03_08.xlsx",index_col=0)

# vols_atm=df.groupby(['ativo_alvo','due_date','category'],as_index=False).agg({
#     'VI_bid': 'mean',
#     'VI_ask': 'mean'
    
# },axis=0)

lista_ordenacao = [
"PETR4",
"BOVA11",
"BOVV11",
"VALE3",
"ENGI11",
"BRFS3",
"MGLU3",
"PRIO3",
"RENT3",
"BBAS3",
"BBDC4",
"ITUB4",
"ABEV3",
"IRBR3",
"EQTL3",
"CSNA3",
"ENEV3",
"MRFG3",
"B3SA3",
"AZUL4",
"LREN3",
"SUZB3",
"PCAR3",
"BPAC11",
"PETR3",
"JBSS3",
"CIEL3",
"SLCE3",
"CPLE6",
"EMBR3",
"BBSE3",
"CVCB3",
"MULT3",
"CMIG4",
"CPFE3",
"BEEF3",
"HAPV3",
"VBBR3",
"PETZ3",
"WEGE3",
"KLBN11",
"MRVE3",
"UGPA3",
"BBDC3",
"ASAI3",
"CSAN3",
"SOMA3",
"RAIZ4",
"RADL3",
"USIM5",
"COGN3",
"YDUQ3",
"ELET3",
"GOAU4",
"SBSP3",
"BRAP4",
"ITSA4",
"VAMO3",
"RDOR3",
"EGIE3",
"TIMS3",
"GOLL4",
"IGTI11",
"RRRP3",
"ALOS3",
"SMTO3",
"VIVT3",
"NTCO3",
"GGBR4",
"SANB11",
"CCRO3",
"TAEE11",
"RECV3",
"BRKM5",
"CYRE3",
"ARZZ3",
"EZTC3",
"LWSA3",
"BHIA3",
"ALPA4",
"HYPE3",
"CRFB3",
"CMIN3",
"FLRY3",
"RAIL3",
"TOTS3",
"ELET6",
"DXCO3"
]


df2= pd.read_excel(r"\\Server\backup usuarios\Base De dados\Base de dados Volatilidade\Base_de_dados_Volatilidade_2024_03_26.xlsx",index_col=0)

# df5= pd.read_excel(r"\\Server\backup usuarios\Base De dados\Base de dados Volatilidade\Base_de_dados_Volatilidade_2024_03_22.xlsx",index_col=0)

df_union=df2
df_union=df_union.reset_index()
vols_atm=df_union.groupby(['ativo_alvo','due_date','category'],as_index=False).agg({
    'VI_bid': 'mean',
    'VI_ask': 'mean'
    
},axis=0)

vols_atm_filtrada=vols_atm[vols_atm['ativo_alvo'].isin(lista_ordenacao)]
vols_atm_filtrada=vols_atm_filtrada.sort_values(by='ativo_alvo')
vols_atm_filtrada=vols_atm_filtrada.query(f"due_date !='2024-03-15'")
vols_atm_filtrada.to_excel('Relatorio Semanal.xlsx')