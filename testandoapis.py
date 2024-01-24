from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import cacluldora_BS as Bs
import yfinance as yf
from plotnine import ggplot, aes, geom_line
driver = webdriver.Chrome()

URL = r"https://opcoes.net.br/login"
driver.get(URL)
time.sleep(1)
login = driver.find_element(By.XPATH,'//*[@id="CPF"]')
login.send_keys('167.640.337-06')
senha = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/section/form/div[2]/input')
senha.send_keys('899513Vi!')
Btn_login = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/section/form/div[4]/button')
Btn_login.click()
url=r'https://opcoes.net.br/opcoes2/bovespa/PETR4'
driver.get(url)
time.sleep(1)
tabela = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/table/tbody")
linhas = tabela.find_elements(By.TAG_NAME, "tr")

data_rows = []  # Create an empty list to store data

for linha in linhas:
    colunas = linha.find_elements(By.TAG_NAME, "td")
    
    # Extract data from each cell and append it to the data_rows list
    row_data = [coluna.text for coluna in colunas]
    data_rows.append(row_data)

# Define column names for your DataFrame
columns = ['Ticker', 'FM', 'Tipo', 'Modelo', 'A/O/ITM', 'strike', 'dist.strike', 'premio', 'ultimo',
           'Num.Nego', 'volume', 'Data/hora', 'vol.imp', 'delta', 'gamma', 'theta', 'vega'
        #    'iq', 'coberto', 'Travado', 'descober', 'titulares', 'lançadores'
           ]

# Create a DataFrame using the collected data and column names
DF_options = pd.DataFrame(data_rows, columns=columns)
parts = url.split('/')
ticker = parts[-1] if parts[-1] else parts[-2]
Ticker_acao = ticker
DF_options["Ticker da Ação"]=Ticker_acao
DF_options["Cotação"]=yf.Ticker(Ticker_acao+'.SA').info['previousClose']
DF_options['ultimo'] = pd.to_numeric(DF_options['ultimo'].str.replace(',', '.'), errors='coerce')
DF_options['strike'] = pd.to_numeric(DF_options['strike'].str.replace(',', '.'), errors='coerce')
DF_options[DF_options["Tipo"]=="CALL"]
DF_options["Vol.Implicita"] = DF_options.apply(
    lambda row: Bs.implied_volatility(row['ultimo'], row['Cotação'], row['strike'], (15/252), 0.1175),
    axis=1
)
DF_options = DF_options[DF_options["Tipo"] == "CALL"]
print(DF_options[['Ticker',"Tipo", 'A/O/ITM','strike','ultimo',"Ticker da Ação","Cotação","Vol.Implicita"]])
p = ggplot(data=DF_options, mapping=aes(x='strike', y='Vol.Implicita')) + geom_line()
print(p)




