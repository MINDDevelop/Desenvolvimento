from openpyxl import load_workbook

# Carregar o arquivo Excel
caminho_do_arquivo = r"C:\Users\vgonçalves\OneDrive\Documents\Planilha final_para testes.xlsx"
workbook = load_workbook(filename=caminho_do_arquivo)

# Acessar a planilha específica pelo nome
nome_da_planilha = 'Base de dados'
sheet = workbook[nome_da_planilha]

# Agora, `sheet` é um objeto Worksheet que representa a planilha específica.
# Você pode ler ou escrever dados nessa planilha como desejar.
# Por exemplo, para ler o valor da célula A1:
valor_a1 = sheet['A1'].value
print(valor_a1)

# E para escrever um valor na célula A2:
sheet['A2'] = 'Novo Valor'

# Não se esqueça de salvar o arquivo se você fez alguma alteração!
workbook.save(filename=caminho_do_arquivo)