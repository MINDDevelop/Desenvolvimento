import sys
import subprocess
import pandas as pd
# from openpyxl import load_workbook

# Lista de pastas onde as instalações do Python estão localizadas
python_folders = [
    r'C:\Users\victo\AppData\Local\Programs\Python\Python311',
    # Adicione outras pastas conforme necessário
]

# Biblioteca que você deseja instalar
library_to_install = 'openpyxl'

for folder in python_folders:
    python_executable = f"{folder}\\python.exe"
    try:
        subprocess.run([python_executable, '-m', 'pip', 'install', library_to_install], check=True)
        print(f"A biblioteca {library_to_install} foi instalada com sucesso em {folder}.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao instalar a biblioteca {library_to_install} em {folder}: {e}")

