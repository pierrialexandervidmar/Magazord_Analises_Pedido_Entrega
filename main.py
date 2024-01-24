"""
Nome do Script: main.py
Autor: Pierri Alexander Vidmar
Data de Criação: 2024-01-01
Versão: 1.0.0

Descrição:
    Este script gera um relatório de entregas com base em dados fornecidos em um arquivo CSV.
    Calcula a média de dias de entrega por estado, o total de entregas dentro do prazo, o estado
    com o maior percentual de atraso, a cidade com o maior percentual de atraso e a percentagem de
    qualidade de entrega.

Dependências:
    - pandas
    - reportlab

Uso:
    Certifique-se de ter os arquivos 'consulta.csv' e 'main.py' no mesmo diretório.
    Execute o script para gerar um arquivo PDF contendo o relatório de entregas.

Exemplo:
    python main.py

"""
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

df = pd.read_csv('consulta.csv', delimiter=';', encoding='latin1')

# Média de dias de entrega por estado
atraso_por_estado = df.groupby('Estado')['Dias para Entrega'].mean().round(2)

# Dataframe com somente o número de registros onde os dias de entrega foram menores ou igual ao prazo estipulado
total_entrega_dentro_prazo = df[df['Dias para Entrega'] <= df['Prazo para Entrega']].shape[0]

# Dataframe com somente o número de registros onde os dias de entrega foram maiores ao prazo estipulado
total_entrega_fora_prazo = df[df['Dias para Entrega'] > df['Prazo para Entrega']].shape[0]

# Pegamos os registros com atrasos, agrupamos por estado, então calculamos a média de atraso de cada estado.
# Ao final devolvemos o estado com o maior valor médio de atraso.
estado_maior_percentual_atraso = (df['Dias para Entrega'] > df['Prazo para Entrega']).groupby(df['Estado']).mean().idxmax()

# Pegamos os registros com atrasos, agrupamos por estado, então calculamos a média de atraso de cada estado.
# Ao final devolvemos o estado com o menor valor médio de atraso.
estado_menor_percentual_atraso = (df['Dias para Entrega'] <= df['Prazo para Entrega']).groupby(df['Estado']).mean().idxmax()

# Pegamos os registros com atrasos, agrupamos por cidade, então calculamos a média de atraso por cidade.
# Ao final devolvemos a cidade com o maior valor médio de atraso. 
cidade_maior_percentual_atraso = (df['Dias para Entrega'] > df['Prazo para Entrega']).groupby(df['Cidade']).mean().idxmax()

# Pegamos os registros com atrasos, agrupamos por cidade, então calculamos a média de atraso por cidade.
# Ao final devolvemos a cidade com o menor valor médio de atraso. 
cidade_menor_percentual_atraso = (df['Dias para Entrega'] <= df['Prazo para Entrega']).groupby(df['Cidade']).mean().idxmax()

# Porcentagem do toal de entregas dentro do prazo
percentual_qualidade_entrega = (total_entrega_dentro_prazo / df.shape[0]) * 100


# Função para criar o PDF
def create_pdf(atraso_por_estado, total_entrega_dentro_prazo, total_entrega_fora_prazo, estado_maior_percentual_atraso,
            estado_menor_percentual_atraso, cidade_maior_percentual_atraso, cidade_menor_percentual_atraso, percentual_qualidade_entrega):
    
    filename = "relatorio_entregas.pdf"
    
    # Inicializa o objeto canvas
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Adiciona título
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 750, "Relatório de Entregas")
    
    # Adiciona os resultados ao PDF
    c.setFont("Helvetica", 12)
    
    # Atraso por Estado
    c.drawString(50, 700, "Média de atraso em dias, por Estado:")
    for i, (estado, atraso) in enumerate(atraso_por_estado.items()):
        c.drawString(70, 680 - i * 20, f"{estado}: {atraso} dias")

    # Calcula o número de estados
    num_estados = len(atraso_por_estado)
    # Ajusta a posição Y da linha total_entrega_dentro_prazo
    y_position_total_entrega = 670 - num_estados * 20
    
    # Total de Entregas dentro do Prazo
    c.drawString(50, y_position_total_entrega, f"Total Dentro do Prazo: {total_entrega_dentro_prazo}")

    # Total de Entregas fora do Prazo
    c.drawString(50, y_position_total_entrega - 20, f"Total Fora do Prazo: {total_entrega_fora_prazo}")
    
    # Estado com Maior Percentual de Atraso
    c.drawString(50, y_position_total_entrega - 40, f"Atraso por Estado %:     Maior: {estado_maior_percentual_atraso}   ||     Menor: {estado_menor_percentual_atraso}")
    
    # Cidade com Maior Percentual de Atraso
    c.drawString(50, y_position_total_entrega - 60, f"Atraso por Cidade %:     Maior: {cidade_maior_percentual_atraso}   ||     Menor: {cidade_menor_percentual_atraso}")
        
    # Percentual de Qualidade de Entrega
    c.drawString(50, y_position_total_entrega - 80, f"Percentual de Qualidade de Entrega: {percentual_qualidade_entrega:.2f}%")

        
    # Salva o arquivo PDF
    c.save()
    print(f"O arquivo {filename} foi gerado com sucesso.")



# Chama a função para criar o PDF
create_pdf(atraso_por_estado, total_entrega_dentro_prazo, total_entrega_fora_prazo, estado_maior_percentual_atraso,
           estado_menor_percentual_atraso, cidade_maior_percentual_atraso, cidade_menor_percentual_atraso, percentual_qualidade_entrega)