import openai
import requests
import json

# Substitua "sua_chave_de_api_aqui" pela sua chave de API da OpenAI,
# ou configure a chave de API como uma variável de ambiente.
api_key = "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"

headers = {'Authorization': f'Bearer {api_key}',"Content-Type": "application/json"}
link = 'https://api.openai.com/v1/chat/completions'

id_modelo="gpt-3.5-turbo"

body_mensagem= {
    "model": id_modelo,
    "messages": [{"role":"user","content": 'baseado na minha api key quais modelo de chat gpt na api do python eu posso usar minha api key é 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'}]
}
body_mensagem=json.dumps(body_mensagem)

requisicao=requests.post(link,headers=headers,data=body_mensagem)
print(requisicao.text)
