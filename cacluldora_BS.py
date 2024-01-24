from scipy.optimize import fsolve
import numpy as np
import scipy.stats as st

def black_scholes_option_price(volatility, S, K, T, r, option_type='call'):
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

    if option_type == 'call':
        option_price = S * st.norm.cdf(d1) - K * np.exp(-r * T) * st.norm.cdf(d2)
    elif option_type == 'put':
        option_price = K * np.exp(-r * T) * st.norm.cdf(-d2) - S * st.norm.cdf(-d1)
    else:
        raise ValueError("option_type deve ser 'call' ou 'put'.")

    return option_price

def implied_volatility(option_price, S, K, T, r, option_type='call'):
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
    implied_volatility = fsolve(objective_function,x0=0.5)[0]

    return implied_volatility*100

