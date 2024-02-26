import Functions as tt 
import cacluldora_BS as BS 
from datetime import datetime,timedelta
import pandas as pd
import numpy as np
import os
from scipy.optimize import fsolve
import numpy as np
import scipy.stats as st
from workalendar.america import Brazil
import pandas as pd
from datetime import datetime,timedelta
import os
from datetime import datetime, timedelta
from datetime import datetime
import requests
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings
from datetime import datetime,timedelta
import os
from matplotlib import style
from workalendar.america import Brazil
import xml.etree.ElementTree as ET
import functools
pd.set_option('display.width', 10000)

caminho=r'C:\Users\vgonçalves\Desktop\Desenvolvimento\Desenvolvimento\Arquivos'

vols=pd.read_excel(rf'{caminho}\Planilha_com_vol.xlsx')
vols['in/on']=vols.apply(tt.determinar_tmoney,axis=1)
vols['VI_bid']=vols['VI_bid']/100
vols['VI_ask']=vols['VI_ask']/100
vols['Dif']=vols['close']* 0.01
vols=vols.query('`Dif.Book`<= Dif ')

vols_atm=vols.groupby(['ativo_alvo','due_date','category','in/on'],as_index=False).agg({
    'VI_bid': 'mean',
    'VI_ask': 'mean'
    
},axis=0)
vols_atm.to_excel(rf'{caminho}\vols_final_mes.xlsx')


