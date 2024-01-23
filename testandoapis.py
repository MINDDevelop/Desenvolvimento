from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
driver = webdriver.Chrome()
URL = r"https://opcoes.net.br/login"
driver.get(URL)
time.sleep(5)
login = driver.find_element(By.XPATH,'//*[@id="CPF"]')
login.send_keys('167.640.337-06')
senha = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/section/form/div[2]/input')
senha.send_keys('899513Vi!')
Btn_login = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/section/form/div[4]/button')
Btn_login.click()
driver.get(r'https://opcoes.net.br/opcoes2/bovespa/PETR4')
tabela = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/table/tbody")
dados = pd.DataFrame({ 
    "Ticker","Tipo","FM","MOD","Strike","IN","Strike","Ultimo","var",''
})
linhas = tabela.find_elements(By.TAG_NAME,"tr")
for linha in linhas: 
    colunas = linha.find_elements(By.TAG_NAME,"td")
    
    # Imprime os dados de cada célula
    for coluna in colunas:
        # Extrai e imprime o texto da célula
        print(coluna.text, end="\t")
    print()

# Fecha o navegador
driver.quit()






