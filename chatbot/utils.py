# chatbot/utils.py
import requests
import json
from decouple import config

def consulta_titulos_api_cnpj(cnpj):

    url = f"{config('DATASUL_HOST')}/esp/combio/v1/api_chatbot/piBuscatitulosCNPJ/"
    payload = json.dumps({
        "cnpj": cnpj
    })
    headers = {
        'Authorization': f'Basic {config('DATASUL_TOKEN')}',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:

        return response.json().get('items', [])
    else:
        return None