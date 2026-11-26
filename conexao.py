
# ============================================================
# BOVINU'S AUGUSTA - CONEXÃO COM MYSQL
# ============================================================

import mysql.connector

# Função responsável por conectar ao banco de dados
def conectar_banco():
    conexao = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",
        database="bobinus_augusta"
    )

    return conexao
