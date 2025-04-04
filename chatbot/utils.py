# chatbot/utils.py
import requests
import json
from decouple import config
from datetime import datetime, timedelta

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


def consulta_titulos_pagos_api(cnpj, data_inicial, data_final):
    url = f"{config('DATASUL_HOST')}/esp/combio/v1/api_chatbot/piBuscatitulosPagosCNPJ/"
    payload = json.dumps({
        "cnpj": cnpj,
        "dataInicial": data_inicial,
        "dataFinal": data_final
    })
    headers = {
        'Authorization': f'Basic {config("DATASUL_TOKEN")}',
        'Content-Type': 'application/json',
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code != 200:
        print("❌ Erro ao consultar títulos pagos:")
        print("Status:", response.status_code)
        print("Resposta:", response.text)
        print("Payload enviado:", payload)

    if response.status_code == 200:
        return response.json().get('items', [])

    return []


def consulta_titulos_api(cnpj):
    url = f"{config('DATASUL_HOST')}/esp/combio/v1/api_chatbot/piBuscatitulosCNPJ/"
    payload = json.dumps({"cnpj": cnpj})
    headers = {
        'Authorization': f'Basic {config('DATASUL_TOKEN')}',
        'Content-Type': 'application/json',
    }
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json().get('items', [])
    return []

def cnpj_valido(cnpj):
    return cnpj.isdigit() and len(cnpj) in [11, 14]

def data_valida(data_str):
    try:
        datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def send_message(to, text):
    token = config('TOKEN_WHATSAPP')
    url = f"https://graph.facebook.com/v20.0/{config('WHATSAPP_ID')}/messages"
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
    }
    data = {
        'messaging_product': 'whatsapp',
        'to': to,
        'type': 'text',
        'text': {'preview_url': False, 'body': text}
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        print("❌ Erro ao enviar mensagem para o WhatsApp:")
        print("Status:", response.status_code)
        print("Resposta:", response.text)
        print("Payload enviado:", json.dumps(data, indent=2))

    return response.json()

MAX_WHATSAPP_CHAR = 4000

def formatar_titulos_em_blocos(titulos):
    """
    Agrupa títulos em blocos de até 4000 caracteres para envio via WhatsApp,
    removendo o campo de valor e formatando cada linha como:
    Cód        Parcela  Emissão      Vencimento
    123456     01       01/04/2025   10/04/2025
    """
    blocos = []
    bloco_atual = ''
    cabecalho = f"{'Cód':<10} {'Parcela':<8} {'Emissão':<12} {'Vencimento':<12}\n"

    for titulo in titulos:
        cod = titulo["cod_tit_ap"]
        parcela = titulo["cod_parcela"]
        emissao = datetime.strptime(titulo["dat_emis_docto"], "%Y-%m-%d").strftime("%d/%m/%Y")
        vencimento = datetime.strptime(titulo["dat_vencto_tit_ap"], "%Y-%m-%d").strftime("%d/%m/%Y")
        linha = f"{cod:<10} {parcela:<8} {emissao:<12} {vencimento:<12}\n"

        if len(bloco_atual) + len(linha) + len(cabecalho) > MAX_WHATSAPP_CHAR:
            blocos.append(cabecalho + bloco_atual.strip())
            bloco_atual = linha
        else:
            bloco_atual += linha

    if bloco_atual.strip():
        blocos.append(cabecalho + bloco_atual.strip())

    return blocos

def formatar_titulos_pagos_em_blocos(titulos):
    blocos = []
    bloco_atual = ''
    cabecalho = f"{'NF.':<10} {'Parcela':<8} {' Emissão':<12} {'  Vencimento':<12} {'  Pagamento':<12}\n"
    
    for titulo in titulos:
        cod = titulo['cod_tit_ap']
        parcela = titulo['cod_parcela']
        emissao = datetime.strptime(titulo['dat_emis_docto'], '%Y-%m-%d').strftime('%d/%m/%Y')
        vencimento = datetime.strptime(titulo['dat_vencto_tit_ap'], '%Y-%m-%d').strftime('%d/%m/%Y')
        pagamento = datetime.strptime(titulo['data_pagamento'], '%Y-%m-%d').strftime('%d/%m/%Y')
        linha = f"{cod:<10} {parcela:<8} {emissao:<12} {vencimento:<12} {pagamento:<12}\n"

        # Verifica se ao adicionar a linha e o cabeçalho ultrapassa o limite
        if len(bloco_atual) + len(linha) + len(cabecalho) > MAX_WHATSAPP_CHAR:
            blocos.append(cabecalho + bloco_atual.strip())
            bloco_atual = linha
        else:
            bloco_atual += linha

    if bloco_atual.strip():
        blocos.append(cabecalho + bloco_atual.strip())

    return blocos