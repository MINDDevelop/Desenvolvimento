from scipy.optimize import fsolve
import numpy as np
import scipy.stats as st
from workalendar.america import Brazil
import pandas as pd
from datetime import datetime,timedelta
import os
from datetime import datetime, timedelta


import requests

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
    return (implied_volatility(linha['ask'],linha['Preco_ativo'],linha['strike'],(quantidades_du(linha['due_date'],datetime.today().strftime("%Y-%m-%d")))/252,0.1125,linha['category']))

def calcular_IV_linha_bid(linha):
    return (implied_volatility(linha['bid'],linha['Preco_ativo'],linha['strike'],(quantidades_du(linha['due_date'],datetime.today().strftime("%Y-%m-%d")))/252,0.1125,linha['category']))

def calcular_IV_nego(linha):
    return (implied_volatility(linha['price'],linha['spot'],linha['strike'],(quantidades_du(linha['Venc.'],datetime.today().strftime("%Y-%m-%d")))/252,0.1125,linha['Tipo']))


def calcular_IV_hist_ask(linha):
    return (implied_volatility(linha['ask'],linha['close'],linha['strike'],(quantidades_du(linha['due_date'],datetime.today().strftime("%Y-%m-%d")))/252,0.1125,linha['category']))
def calcular_IV_hist_bid(linha):
    return (implied_volatility(linha['bid'],linha['close'],linha['strike'],(quantidades_du(linha['due_date'],datetime.today().strftime("%Y-%m-%d")))/252,0.1125,linha['category']))

def calcular_du(linha):
    hoje = datetime.now().date()
    return(quantidades_du(linha['due_date'],hoje))

# def calcular_bs_bid(linha):
#     if pd.notna(linha[0, 'VI_ask']):
#         return(black_scholes_option_price(linha['VI_ask'],linha['close'],linha['strike'],linha['days_to_maturity']/252,0.1175))
#     else:
#         return np.nan
def calcular_bs_ask(linha):
    if pd.notna(linha['VI_ask']):
        # Faça algo se a coluna 'VI_ask' não for vazia
        return(black_scholes_option_price(linha['VI_ask'],linha['close'],linha['strike'],(linha['days_to_maturity']/252),0.1175,linha['category']))
    else:
        # Faça algo se a coluna 'VI_ask' for vazia
        return np.nan
def calcular_bs_bid(linha):
    if pd.notna(linha['VI_bid']):
        # Faça algo se a coluna 'VI_ask' não for vazia
        return(black_scholes_option_price(linha['VI_bid'],linha['close'],linha['strike'],(linha['days_to_maturity']/252),0.1175,linha['category']))
    else:
        # Faça algo se a coluna 'VI_ask' for vazia
        return np.nan
    
def calcular_du2(linha):
    hoje = datetime.now().date()
    return(quantidades_du(linha['Vencimento'],hoje))


def calcular_IV_new_Bid(linha):
    return (implied_volatility(linha['Bid'],linha['Preco_Ref'],linha['Strike'],(linha['days_to_maturity'])/252,0.1125,linha['tipo']))

def calcular_IV_new_ask(linha):
    return (implied_volatility(linha['Ask'],linha['Preco_Ref'],linha['Strike'],(linha['days_to_maturity'])/252,0.1125,linha['tipo']))

def calculo_delta(volatility, S, K, T, r, option_type):
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
    

    if option_type == 'CALL':
        delta = st.norm.cdf(d1)
        
    elif option_type == 'PUT':
        delta = st.norm.cdf(d1) - 1
        
    else:
        raise ValueError("option_type deve ser 'CALL' ou 'PUT'.")

    return delta*100

def calcular_delta_Bid(linha):
    return calculo_delta(linha['VI_bid'], linha['close'], linha['strike'], (linha['days_to_maturity'])/252, 0.1125, linha['category'])

def calcular_delta_Ask(linha):
    return calculo_delta(linha['VI_ask'], linha['close'], linha['strike'], (linha['days_to_maturity'])/252, 0.1125, linha['category'])