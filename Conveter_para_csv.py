import pandas as pd
import os
from datetime import datetime
import cacluldora_BS as BS 
import re
import Functions as tt

def xlsx_to_csv(folder_path):
    # Expressão regular para encontrar a data no formato YYYY-MM-DD no nome do arquivo
    date_pattern = re.compile(r'\d{4}_\d{2}_\d{2}')

    # Lista todos os arquivos na pasta especificada
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.xlsx'):
            # Extrair a data do nome do arquivo
            date_match = date_pattern.search(file_name)
            if date_match:
                file_date = date_match.group()
            else:
                file_date = datetime.today().strftime('%Y-%m-%d')
                print(f"Data não encontrada no nome do arquivo {file_name}, usando data atual: {file_date}")

            # Caminho completo do arquivo
            file_path = os.path.join(folder_path, file_name)

            # Ler o arquivo xlsx usando pandas
            df = pd.read_excel(file_path, engine='openpyxl')
            df['data'] = file_date.replace('_','-')  # Usar a data extraída do nome do arquivo
            df['tmoney']=''
            # Selecionar as colunas desejadas
            tabela = df[['data','ativo_alvo','symbol','category','strike','close','due_date',
                     'days_to_maturity','tmoney','in/on','bid','ask','VI_bid','VI_ask',
                     'delta_bid','delta_ask']]

            # Criar um novo nome de arquivo com extensão .csv
            csv_file_name = file_name.replace('.xlsx', '.csv')
            csv_file_path = os.path.join(folder_path, csv_file_name)

            # Salvar o DataFrame como CSV
            tabela.to_csv(rf'\\WIN-RJAPD707RCN\Arquivos_bulk\Base de dados Sem Vols\{csv_file_name}', index=False)
            print(f"Convertido {file_name} para {csv_file_name}")


ab=pd.read_csv(r'C:\Users\vgoncalves\Downloads\13-05-2024_NEGOCIOSAVISTA\13-05-2024_NEGOCIOSAVISTA.txt',sep=';')
ab.to_csv(r'\\WIN-RJAPD707RCN\Arquivos_bulk\BASE DE OPCOES B3\Negociacao.csv',index=False)


