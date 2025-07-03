# No que consiste a automação:
# abrir um arquivo TXT com varios CNPJS
# consultar cada CNPJ na API do Invertexto
# salvar o resultado da consulta no banco MySQL
# Só devem ser consultados os novos dados inseridos
import re
import requests
from tokenCNPJ import API_TOKEN
import pymysql

def conectar_banco():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='admin',
        port=3306,
        database='cnpjs',
    )
    conn_cursor = conn.cursor()
    return conn, conn_cursor

#verificar se o cnpj já está no banco
def verificar_cnpj(cnpj):
    conexao_consulta, cursor_consulta = conectar_banco()
    query = '''
        SELECT COUNT(*) FROM cnpjs
        WHERE cnpj = %s
        '''
    cursor_consulta.execute(query, (cnpj,))
    resultado = int(cursor_consulta.fetchone()[0]) > 0
    cursor_consulta.close()
    conexao_consulta.close()
    return resultado


cnpjs = open(r'C:\Users\Thomas\Desktop\pythonAuto\cnpj.txt', 'r').read().splitlines()

for cnpj in cnpjs:

    # remover caracteres não númericos do CNPJ
    cnpj_corrigido = re.sub(r'\D', '', cnpj)
    if verificar_cnpj(cnpj_corrigido):
        print(f'cnpj {cnpj} já cadastrado')
        continue

    # consultar API
    response = requests.get(f'https://api.invertexto.com/v1/cnpj/{cnpj_corrigido}?token={API_TOKEN}')
    if response.status_code == 200:
        dados = response.json()
        razao_social, data_inicio = dados['razao_social'], dados['data_inicio']
        conexao, cursor = conectar_banco()

        # Instrução SQL para inserir no banco: %s serve como máscara para ser substituído no comando cursor.execute
        query = 'INSERT INTO cnpjs (cnpj, razaoSocial, dataInicio) VALUES (%s, %s, %s);'
        valores = (cnpj_corrigido, razao_social, data_inicio)
        cursor.execute(query, valores) #Executar a instrução SQL
        conexao.commit()
        # fechar conexão e cursor
        cursor.close()
        conexao.close()
        continue
    elif response.status_code == 422:
        print(f'CNPJ {cnpj} não foi encontrado')
    else:
        print(response.status_code)
        print(response.text)
