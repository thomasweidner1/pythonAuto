import requests
from tokenCNPJ import API_TOKEN

cnpj = '41125383000101'
response = requests.get(f'https://api.invertexto.com/v1/cnpj/{cnpj}?token={API_TOKEN}')

if response.status_code == 200:
    print(response.text)
