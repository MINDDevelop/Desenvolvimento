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
for i in vencimentos:
    tabela_filtrado=tabela.query(rf"category == 'CALL' & due_date == '{i}' & volume > 10000 & moneyness =='ATM'")
    if not tabela_filtrado.empty:
        tabela_filtrado.to_csv(rf'{Ticker}_{i}_CALL.csv')
for i in vencimentos:
    tabela_filtrado=tabela.query(rf"category == 'PUT' & due_date == '{i}' & volume > 10000 & moneyness =='ATM'")
    if not tabela_filtrado.empty:
        tabela_filtrado.to_csv(rf'{Ticker}_{i}_PUT.csv') 
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

# print(df_vols)
