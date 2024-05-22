import Functions as tt
import pandas as pd
import yaml
import MetaTrader5 as mt5
tabela =tt.acoes_options()
# price=pd.DataFrame(tt.acoes_options())
# price=price.rename(columns={
#      'symbol':'ativo_alvo'})
# all_options=pd.DataFrame(columns=['symbol','category','strike',
#                                   'due_date','ativo_alvo'])
# for ativos in tabela['symbol']:
#     print('fazendo com o ticker',ativos)

#     tabela=tt.opcoes_ativos23(ativos)
#     tabela=pd.DataFrame(tabela)
#     tabela['ativo_alvo']=str(ativos)
    
#     df=pd.merge(tabela,price,on='ativo_alvo',how='inner')
#     all_options=pd.concat([all_options,df])
# all_options.to_csv('Base_opcoes_oplab.csv',index=False)




# def spot(symbol):
#     with open(r'\\MIND_INTERNO\Users\Public\Pictures\Nova pasta\senha.yaml', 'r') as arquivo:
       
#        dados = yaml.load(arquivo, Loader=yaml.FullLoader)
#     login=dados['login'] 
#     password=dados['password']
#     server=dados['server']
#     mt5.initialize(login=login, password=password, server=server)
#     mt5.symbol_select(symbol, True)
    
#     return mt5.symbol_info_tick(symbol).last

with open(r'\\MIND_INTERNO\Users\Public\Pictures\Nova pasta\senha.yaml', 'r') as arquivo:
    dados = yaml.load(arquivo, Loader=yaml.FullLoader)
login=dados['login'] 
password=dados['password']
server=dados['server']
mt5.initialize(login=login, password=password, server=server)

symbols = mt5.symbols_get()

# Limpar observações para cada símbolo
for symbol in symbols:
    result = mt5.symbol_select(symbol.name, False)
    if not result:
        print(f"Falha ao limpar observação para o símbolo: {symbol.name}")
mt5.shutdown()
print("Observações limpas com sucesso!")


     
     

