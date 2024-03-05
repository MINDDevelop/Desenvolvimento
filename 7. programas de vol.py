import tkinter as tk
from tkinter import ttk
import pandas as pd

def ler_excel(caminho_arquivo):
    return pd.read_excel(caminho_arquivo, index_col=0)

# Carrega os dados do Excel
df = ler_excel(r"\\Server\backup usuarios\Base De dados\Base de dados Completa\Base_de_dados_2024_02_29.xlsx")


# Inicializa a interface gráfica Tkinter
root = tk.Tk()
root.geometry("800x600")
root.title("Visualizador de Dados DataFrame")
tree = ttk.Treeview(root)
# Dicionário para manter os widgets de informações (Labels)
informacoes = {}

# Função para atualizar a combobox de due_date e iniciar a atualização da combobox de strikes
def atualizar_due_date_combobox(event):
    # Limpa a combobox_due_date antes de preencher
    combobox_due_date['values'] = []
    
    # Obtém o ativo_alvo selecionado
    ativo_alvo_selecionado = combobox_ativo_alvo.get()
    
    # Filtra o DataFrame para o ativo_alvo selecionado
    datas_disponiveis = df[df['ativo_alvo'] == ativo_alvo_selecionado]['due_date'].dropna().unique()
    datas_disponiveis = [str(data) for data in datas_disponiveis]  # Converte as datas para string
    
    # Atualiza a combobox_due_date com as datas disponíveis
    combobox_due_date['values'] = datas_disponiveis
    
    # Se existirem datas disponíveis, define a primeira como selecionada e atualiza os strikes
    if datas_disponiveis:
        combobox_due_date.set(datas_disponiveis[0])
        atualizar_strikes(None)  # Atualiza os strikes aqui
    else:
        combobox_due_date.set('')
def make_entry_readonly(entry):
    entry.configure(state='readonly')

# Função para tornar um Entry widget editável (necessário para atualizar o texto)
def make_entry_editable(entry):
    entry.configure(state='normal')
# Função para atualizar a combobox de strikes com base no ativo_alvo e due_date selecionados
def atualizar_strikes(event):
    # Limpa a combobox_strikes antes de preencher
    combobox_strikes['values'] = []
    
    # Obtém os valores selecionados
    ativo_alvo_selecionado = combobox_ativo_alvo.get()
    due_date_selecionada = combobox_due_date.get()
    
    # Filtra o DataFrame para os strikes disponíveis com base no ativo_alvo e due_date
    strikes_disponiveis = df[(df['ativo_alvo'] == ativo_alvo_selecionado) & (df['due_date'].astype(str) == due_date_selecionada)]['strike'].dropna().unique()
    strikes_disponiveis = [str(strike) for strike in strikes_disponiveis]  # Converte os strikes para string
    
    # Atualiza a combobox_strikes com os strikes disponíveis
    combobox_strikes['values'] = strikes_disponiveis
    
    # Se existirem strikes disponíveis, define o primeiro como selecionado
    if strikes_disponiveis:
        combobox_strikes.set(strikes_disponiveis[0])
    else:
        combobox_strikes.set('')
    for i, coluna in enumerate(df.columns):
        label = tk.Label(root, text=f'{coluna}:')
        label.grid(row=i+1, column=0, sticky='e', padx=10, pady=2)
        info_label = tk.Label(root, text='')
        info_label.grid(row=i+1, column=1, sticky='w', padx=10, pady=2)
        informacoes[coluna] = info_label
def atualizar_informacoes(event):
    ativo_alvo_selecionado = combobox_ativo_alvo.get()
    due_date_selecionada = combobox_due_date.get()
    strike_selecionado = combobox_strikes.get()

    # Filtra o DataFrame com base nas seleções
    dados_filtrados = df[(df['ativo_alvo'] == ativo_alvo_selecionado) & 
                         (df['due_date'].astype(str) == due_date_selecionada) &
                         (df['strike'].astype(str) == strike_selecionado)]

    # Verifica se há dados após o filtro
    if not dados_filtrados.empty:
        linha = dados_filtrados.iloc[0]
        for coluna in df.columns:
            informacoes[coluna].config(text=f'{linha[coluna]}')
    else:
        # Limpa as labels se não houver dados correspondentes
        for coluna in df.columns:
            informacoes[coluna].config(text='')
def atualizar_treeview():
    # Limpa o Treeview
    for i in tree.get_children():
        tree.delete(i)
    
    # Filtra o DataFrame com base nas seleções
    ativo_alvo_selecionado = combobox_ativo_alvo.get()
    due_date_selecionada = combobox_due_date.get()
    strike_selecionado = combobox_strikes.get()
    
    dados_filtrados = df[(df['ativo_alvo'] == ativo_alvo_selecionado) & 
                         (df['due_date'].astype(str) == due_date_selecionada) &
                         (df['strike'].astype(str) == strike_selecionado)]
    
    # Atualiza o Treeview com os dados filtrados
    for index, row in dados_filtrados.iterrows():
        tree.insert("", tk.END, values=list(row))   
def inicializar_treeview():
    global tree
    tree = ttk.Treeview(root, columns=list(df.columns), show="headings")
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.grid(row=4, column=0, columnspan=3, sticky='nsew')
inicializar_treeview()

# Combobox para a coluna ativo_alvo
opcoes_ativo_alvo = df['ativo_alvo'].dropna().unique().tolist()
combobox_ativo_alvo = ttk.Combobox(root, values=opcoes_ativo_alvo)
combobox_ativo_alvo.grid(row=0, column=0, padx=10, pady=10)
combobox_ativo_alvo.bind('<<ComboboxSelected>>', atualizar_due_date_combobox)

# Combobox para a coluna due_date, inicialmente vazia
combobox_due_date = ttk.Combobox(root, state="readonly")
combobox_due_date.grid(row=0, column=1, padx=10, pady=10)
combobox_due_date.bind('<<ComboboxSelected>>', atualizar_strikes)  # Atualiza os strikes quando uma due_date é selecionada

# Combobox para a coluna strike, inicialmente vazia
combobox_strikes = ttk.Combobox(root, state="readonly")
combobox_strikes.grid(row=0, column=2, padx=10, pady=10)
combobox_strikes.bind('<<ComboboxSelected>>', lambda e: atualizar_treeview())

# Cria Labels para as informações das colunas
for i, coluna in enumerate(df.columns):
    label = tk.Label(root, text=f'{coluna}:')
    label.grid(row=i+1, column=0, sticky='e', padx=10, pady=2)
    info_entry = tk.Entry(root)
    info_entry.grid(row=i+1, column=1, sticky='w', padx=10, pady=2)
    make_entry_readonly(info_entry)  # Torna o Entry somente leitura
    informacoes[coluna] = info_entry

root.mainloop()
