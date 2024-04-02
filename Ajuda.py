import requests
def get_token(email,senha): #OK
    
    body = {"email": email,"password": senha}
    
    ## CHAMADA NA API
    r = requests.post('https://api.oplab.com.br/v3/domain/users/authenticate',json=body).json()['access-token']
    return r

email='victor.drone2013@gmail.com'
senha='899513Vi!'
Token=get_token(email,senha)

def Cotacoes(symbol):  #OK
    
    """
    symbol= ticker da ação que queremos ver as opções

    Retorna:
    - pegamos a cotação do ativo. caso o mercado esteja fechado usamos o ultimo preço de fechamento do ativo

    """
    
    header = {"Access-Token": Token}
    
    ## CHAMADA NA API 
    dados = requests.get('https://api.oplab.com.br/v3/market/stocks/{}'.format(symbol),headers=header).json()  
    return dados.get('close')
print(Cotacoes('HAPV3'))

