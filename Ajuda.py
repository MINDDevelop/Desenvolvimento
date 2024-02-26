###############################################################################################
#                            plotar os graficos                                               #  
###############################################################################################
# for i in vencimentos:
#     tabela_filtrado=tabela.query(rf"category == 'CALL' & due_date == '{i}' & volume > 100 & moneyness =='ATM'")
    
#     if not tabela_filtrado.empty:
#     # Plotar a curva de volatilidade para o vencimento atual
#         tabela_filtrado["volatility_implicita_media_ask"] = tabela_filtrado.groupby("strike")["Volatilidade Implicita(ask)"].transform("mean")
#         tabela_filtrado["volatility_implicita_media_bid"] = tabela_filtrado.groupby("strike")["Volatilidade Implicita(bid)"].transform("mean")
#         tabela_filtrado.sort_values(by="strike")
#         unique_strikes = tabela_filtrado["strike"].unique()
#         plt.plot( tabela_filtrado["strike"],tabela_filtrado['volatility_implicita_media_ask'], label=f"{i}_normal")
#     if len(unique_strikes) < 2:
#         print("Error: At least 2 unique strike values are required for CubicSpline.")
#     else:
#         # Create the spline only if there are at least 2 unique strike values
#         spline = CubicSpline(tabela_filtrado["strike"], tabela_filtrado["volatility_implicita_media_ask"])
        
        
#         # Gere valores suavizados usando o spline
#         strike_smooth = np.linspace(tabela_filtrado["strike"].min(), tabela_filtrado["strike"].max(), 1000)
#         volatility_smooth = spline(strike_smooth)
#         print(strike_smooth,volatility_smooth)
    
#         plt.plot(strike_smooth, volatility_smooth, label=f"{i} Suavizado")
# # Adicionar rótulos e legendas ao gráfico

# plt.xlabel("Strike")
# plt.ylabel("Vol.Média")
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
# plt.title("Curvas de Volatilidade para Diferentes Vencimentos")
# plt.grid(True)
# plt.show()
###############################################################################################
#                            CSV das Vol implicitas                                           #  
###############################################################################################

###############################################################################################
#                            Calculo da media e desvio padrao                                 #  
###############################################################################################
# df_vols = pd.DataFrame(columns=['Data do Strike', 'Volatilidade Implicita(ask)', 'Volatilidade Implicita(bid)','DP ask','DP Bid'])
# for i in vencimentos:
#     tabela_filtrada = tabela.query(f"(category == 'CALL') & (due_date == '{i}') & (volume > 100000) & (moneyness == 'ATM')")
#     med_ask_c = tabela_filtrada['Volatilidade Implicita(ask)'].mean()
#     med_bid_c = tabela_filtrada['Volatilidade Implicita(bid)'].mean()
#     dp_ask_c = tabela_filtrada['Volatilidade Implicita(ask)'].std()
#     dp_bid_c = tabela_filtrada['Volatilidade Implicita(bid)'].std()
    
    
    
#     df_vols.loc[len(df_vols)] = [i, med_ask_c, med_bid_c,dp_ask_c,dp_bid_c]

import pandas as pd
import matplotlib.pyplot as plt
# print(df_vols)
df=pd.read_csv(r"C:\Users\vgonçalves\Desktop\Desenvolvimento\Desenvolvimento\Arquivos\Base_de_dados_MM.csv")
df_filtrado = df[df['Ticker'].str.startswith('PETR')]
df_filtrado['Vencimento'] = pd.to_datetime(df_filtrado['Vencimento'])
df_filtrado=df_filtrado.sort_values(by='Vencimento').query("tipo == 'CALL'")
print(df_filtrado)
plt.plot(df_filtrado['Vencimento'],df_filtrado['VI_ask'],label='VI_ask')
plt.plot(df_filtrado['Vencimento'],df_filtrado['VI_bid'],label='VI_bid')
plt.xlabel("Strike")
plt.ylabel("Vol.Média")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.title("Curvas de Volatilidade para Diferentes Vencimentos")
plt.grid(True)
plt.show()
