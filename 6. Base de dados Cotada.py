import Functions as tt
import pandas as pd
from datetime import datetime
import cacluldora_BS as BS
pd.set_option('display.width', 10000)
while True:
    db_cotadas=pd.read_csv(r'C:\Users\vgonçalves\Desktop\Desenvolvimento\Desenvolvimento\Arquivos\Base_de_dados_MM.csv',index_col=0)
    Ticker = input("Qual o Ticker da Opção: ")
    p_ref = float(input("Qual o preco de referencia do ativo alvo da Opção: "))
    ask = float(input("Qual o ask da Opção: "))  # Corrigido para ser específico ao ask
    bid = float(input("Qual o bid da Opção: "))  # Corrigido para ser específico ao bid
    Data_hoje = datetime.today().strftime('%Y-%m-%d')  # Formatando para string no formato de data
    Vencimento= tt.Consultas_opção_venc(Ticker)
    Strike=tt.Consultas_opção_strike(Ticker)
    Tipo=tt.Consultas_opção_tipo(Ticker)
    novo_registro = pd.DataFrame({
        'Ticker': [Ticker],
        'Preco_Ref': [p_ref],
        'Ask': [ask],
        'Bid': [bid],
        'Data_Hoje': [Data_hoje]
        ,'Vencimento':[Vencimento]
        ,'Strike': [Strike]
        ,'days_to_maturity': ''
        ,'VI_ask':''
        ,'VI_bid':''
        ,'tipo': [Tipo]
    })
    # Adicionando o novo registro ao DataFrame usando pd.concat
    novo_registro['Vencimento'] = pd.to_datetime(novo_registro['Vencimento']).dt.date
    novo_registro['days_to_maturity']=novo_registro.apply(BS.calcular_du2,axis=1)
    novo_registro['VI_ask']=novo_registro.apply(BS.calcular_IV_new_ask,axis=1)
    novo_registro['VI_bid']=novo_registro.apply(BS.calcular_IV_new_Bid,axis=1)
    novo_registro= novo_registro[['Data_Hoje','Ticker','tipo','Strike','Bid','Ask','Vencimento','Preco_Ref','days_to_maturity','VI_ask','VI_bid']]
    db_cotadas = pd.concat([db_cotadas, novo_registro], ignore_index=True)
    db_cotadas.to_csv(r'C:\Users\vgonçalves\Desktop\Desenvolvimento\Desenvolvimento\Arquivos\Base_de_dados_MM.csv')
    resposta=input("tem mais algum ativo a ser inserido Y/N ")
    if resposta =='Y':
        pass
    else:
        break
# print(db_cotadas)






