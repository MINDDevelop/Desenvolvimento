from scipy.optimize import fsolve
import numpy as np
import scipy.stats as st
from workalendar.america import Brazil
import pandas as pd
from datetime import datetime,timedelta

def quantidades_du(Data1,Data2):
    cal = Brazil()
    Data1 = pd.to_datetime(Data1)
    Data2 = pd.to_datetime(Data2)
    dias_uteis = cal.get_working_days_delta(Data1, Data2)
    return(dias_uteis)


def black_scholes_option_price(volatility, S, K, T, r, option_type):
    """
    Calcula o preço teórico de uma opção usando a fórmula de Black-Scholes.

    Parâmetros:
    - volatility: Volatilidade implícita
    - S: Preço atual da ação
    - K: Preço de exercício da opção
    - T: Tempo até o vencimento em anos
    - r: Taxa de juros livre de risco
    - option_type: 'call' para opção de compra, 'put' para opção de venda

    Retorna:
    - O preço teórico da opção
    """
    d1 = (np.log(S / K) + (r + 0.5 * volatility ** 2) * T) / (volatility * np.sqrt(T))
    d2 = d1 - volatility * np.sqrt(T)

    if option_type == 'CALL':
        option_price = S * st.norm.cdf(d1) - K * np.exp(-r * T) * st.norm.cdf(d2)
    elif option_type == 'PUT':
        option_price = K * np.exp(-r * T) * st.norm.cdf(-d2) - S * st.norm.cdf(-d1)
    else:
        raise ValueError("option_type deve ser 'CALL' ou 'PUT'.")

    return option_price

def implied_volatility(option_price, S, K, T, r, option_type):
    #option_price
    
    """
    Calcula a volatilidade implícita usando a fórmula de Black-Scholes e fsolve.

    Parâmetros:
    - option_price: O preço de mercado da opção 
    - S: Preço atual da ação
    - K: Preço de exercício da opção
    - T: Tempo até o vencimento em anos
    - r: Taxa de juros livre de risco
    - option_type: 'call' para opção de compra, 'put' para opção de venda

    Retorna:
    - A volatilidade implícita
    """
    objective_function = lambda volatility: \
        black_scholes_option_price(volatility, S, K, T, r, option_type) - option_price

    # Use fsolve para encontrar a raiz (volatilidade implícita)
    implied_volatility = fsolve(objective_function,x0=0.2)[0]

    return implied_volatility*100
##

###
def calcular_IV_linha_ask(linha):
    return (implied_volatility(linha['ask'],linha['Preco_ativo'],linha['strike'],(quantidades_du(linha['due_date'],datetime.today().strftime("%Y-%m-%d")))/252,0.1175,linha['category']))

def calcular_IV_linha_bid(linha):
    return (implied_volatility(linha['bid'],linha['Preco_ativo'],linha['strike'],(quantidades_du(linha['due_date'],datetime.today().strftime("%Y-%m-%d")))/252,0.1175,linha['category']))