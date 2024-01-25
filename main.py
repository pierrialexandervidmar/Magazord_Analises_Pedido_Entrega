"""
Nome do Script: main.py
Autor: Pierri Alexander Vidmar
Data de Criação: 2024-01-01
Versão: 1.0.0

Descrição:
    Este script gera um relatório de entregas com base em dados fornecidos em um arquivo CSV.
    Calcula a média de dias de entrega por estado, região e transportadora, o total de entregas dentro do prazo, o estado
    com o maior percentual de atraso, a região com o maior percentual de atraso, a transportadora com o maior percentual de atraso,
    a cidade com o maior percentual de atraso e a percentagem de qualidade de entrega.

Dependências:
    - pandas
    - reportlab

Uso:
    Certifique-se de ter os arquivos 'consulta.csv' e 'main.py' no mesmo diretório.
    Execute o script para gerar um arquivo PDF contendo o relatório de entregas.

Exemplo:
    python main.py
"""
import subprocess

# Chama o script para criar o PDF em um novo processo
process = subprocess.Popen(["python3", "script.py"])

# Aguarda o término do processo secundário
process.communicate()

# Imprime em tela após a conclusão do processo secundário
print("Relatório criado com sucesso!")