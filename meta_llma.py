from requests.auth import HTTPBasicAuth
import requests

url = "http://172.16.0.15/ocsapi/v1/computers?start=0&limit=1000"
username = "ocsapi"
password = "ocsapi"

print("entrou no populate_hardware")


response = requests.get(url, auth=HTTPBasicAuth(username, password))
response_data = response.json()
print(response_data)