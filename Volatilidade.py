import Teste as tt 
import cacluldora_BS as BS 
from datetime import datetime,timedelta
import requests
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from scipy import interpolate
import numpy as np
from scipy.interpolate import CubicSpline

pd.set_option('display.width', 10000)
email='victor.drone2013@gmail.com'
senha='899513Vi!'
Token=tt.get_token(email,senha)
tabela=tt.opcoes_ativos(Token,'MGLU3')
tabela['Preco_ativo']=tt.Cotacoes(Token,'MGLU3')
