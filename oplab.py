import Teste as tt 
from datetime import datetime,timedelta

email='victor.drone2013@gmail.com'
senha='899513Vi!'
Token=tt.get_token(email,senha)

print(tt.Cotacoes(Token,'PETR4'))



