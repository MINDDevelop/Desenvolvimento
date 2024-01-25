import matplotlib.pyplot as plt
# Cria uma lista com os vencimentos
vencimentos = ["2024-02-16", "2024-03-15", "2024-04-19"]

# Cria uma lista com as porcentagens de strikes
porcentagens = [38.0, 38.0, 34.0]

# Cria um gráfico de barras
plt.plot(vencimentos, porcentagens)

# Adiciona um título ao gráfico
plt.title("Petra - Skew")

# Exibe o gráfico
plt.show()