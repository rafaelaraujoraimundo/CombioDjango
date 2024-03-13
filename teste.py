from requests_oauthlib import OAuth1Session
CLIENT_KEY = 'combio-talend-secret' #servidorFluig.client_key
CONSUMER_SECRET = 'combio-talend-secret' #servidorFluig.consumer_secret
ACCESS_TOKEN = 'cb5de9d9-718f-4944-a8f0-f71bece358f4'
ACCESS_SECRET = 'b5b85c02-0f69-4a6e-9b63-b3857faa9560fd432e27-9cd4-4257-8e65-dbd06cf74609' #servidorFluig.access_secret
url = 'https://combioenergia.fluig.cloudtotvs.com.br/monitoring/api/v1/statistics/report/'


CLIENT_KEY='combio-talend-secret'
CONSUMER_SECRET='combio-talend-secret'
ACCESS_TOKEN='cb5de9d9-718f-4944-a8f0-f71bece358f4'
ACCESS_SECRET='b5b85c02-0f69-4a6e-9b63-b3857faa9560fd432e27-9cd4-4257-8e65-dbd06cf74609'


print(url)
oauth = OAuth1Session(CLIENT_KEY, client_secret=CONSUMER_SECRET, resource_owner_key=ACCESS_TOKEN, resource_owner_secret=ACCESS_SECRET)
response = oauth.get(url)

if response.status_code == 200:
    print(response)
else:
    print('Erro na requisição:', response.status_code)
    print('Erro na requisição:', response)
    """for i in range(1, 21):  # 10 tentativas no máximo
        print('Tentativa', i)
        time.sleep(30)  # Aguarda 10 minutos (600 segundos)
        response = oauth.post(url, data=body_json, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            return response"""
    
    print('Não foi possível obter uma resposta adequada após 10 tentativas.')