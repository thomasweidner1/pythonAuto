import requests

ceps = open('ceps.txt', 'r').read().splitlines()

cep = str(input("insira o seu cep"))
ceps.append(cep)

for cep in ceps:
    response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
    if response.status_code == 200:
        dados = response.json()
        if 'erro' in dados.keys():
            print(f"CEP {cep} não existe")
            continue
        print(dados)
    else:
        print('Erro na consulta')
