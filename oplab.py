import pandas as pd
import tkinter as tk
from tkinter import ttk
import pandas as pd


# Criar um DataFrame do pandas para exemplo
data = {'Nome': ['Ana', 'Bruno', 'Carlos'],
        'Idade': [25, 30, 22],
        'Cidade': ['Lisboa', 'Porto', 'Coimbra']}
df = pd.DataFrame(data)

# Função para buscar e exibir dados
def buscar_dados():
    # Obter o índice/valor da entrada do usuário
    entrada_usuario = entry_busca.get()
    
    # Buscar no DataFrame. Aqui estamos assumindo entrada_usuario como um índice direto.
    # Adapte a lógica de busca conforme necessário.
    try:
        resultado = df.loc[int(entrada_usuario)]
        # Atualizar os widgets de exibição com os dados encontrados
        label_nome.config(text=resultado['Nome'])
        label_idade.config(text=resultado['Idade'])
        label_cidade.config(text=resultado['Cidade'])
    except (KeyError, ValueError, IndexError):
        # Limpar os labels se a busca falhar ou for inválida
        label_nome.config(text="Não encontrado")
        label_idade.config(text="")
        label_cidade.config(text="")

# Criar a janela principal
root = tk.Tk()
root.title("Busca no DataFrame")
root.geometry("300x200")

# Widget de entrada para a busca
entry_busca = tk.Entry(root)
entry_busca.pack(pady=10)

# Botão para executar a busca
button_busca = tk.Button(root, text="Buscar", command=buscar_dados)
button_busca.pack(pady=5)

# Labels para exibir os resultados da busca
label_nome = tk.Entry(root, text="Nome")
label_nome.pack(pady=3)

label_idade = tk.Entry(root, text="Idade")
label_idade.pack(pady=3)

label_cidade = tk.Entry(root, text="Cidade")
label_cidade.pack(pady=3)

# Executar o loop principal
root.mainloop()