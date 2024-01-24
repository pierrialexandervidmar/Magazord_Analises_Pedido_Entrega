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

# Média de dias de entrega por regiao
atraso_por_regiao = df.groupby('Região')['Dias para Entrega'].mean().round(2)

# Média de dias de entrega por transportadora
atraso_por_transportadora = df.groupby('Transportadora')['Dias para Entrega'].mean().round(2)

# Dataframe com somente o número de registros onde os dias de entrega foram menores ou igual ao prazo estipulado
total_entrega_dentro_prazo = df[df['Dias para Entrega'] <= df['Prazo para Entrega']].shape[0]

# Dataframe com somente o número de registros onde os dias de entrega foram maiores ao prazo estipulado
total_entrega_fora_prazo = df[df['Dias para Entrega'] > df['Prazo para Entrega']].shape[0]

# Pegamos os registros com atrasos, agrupamos por estado, então calculamos a média de atraso de cada estado.
# Ao final devolvemos o estado com o maior valor médio de atraso.
estado_maior_percentual_atraso = (df['Dias para Entrega'] > df['Prazo para Entrega']).groupby(df['Estado']).mean().idxmax()

# Pegamos os registros com atrasos, agrupamos por estado, então calculamos a média de atraso de cada região.
# Ao final devolvemos o região com o maior valor médio de atraso.
regiao_maior_percentual_atraso = (df['Dias para Entrega'] > df['Prazo para Entrega']).groupby(df['Região']).mean().idxmax()

# Pegamos os registros com atrasos, agrupamos por estado, então calculamos a média de atraso de cada estado.
# Ao final devolvemos o estado com o menor valor médio de atraso.
estado_menor_percentual_atraso = (df['Dias para Entrega'] <= df['Prazo para Entrega']).groupby(df['Estado']).mean().idxmax()

# Pegamos os registros com atrasos, agrupamos por estado, então calculamos a média de atraso de cada região.
# Ao final devolvemos o região com o menor valor médio de atraso.
regiao_menor_percentual_atraso = (df['Dias para Entrega'] <= df['Prazo para Entrega']).groupby(df['Região']).mean().idxmax()

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
            estado_menor_percentual_atraso, cidade_maior_percentual_atraso, cidade_menor_percentual_atraso, regiao_maior_percentual_atraso, 
            regiao_menor_percentual_atraso, atraso_por_regiao, atraso_por_transportadora, percentual_qualidade_entrega):
    
    filename = "relatorio_entregas.pdf"
    
    # Inicializa o objeto canvas
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Adiciona título
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 750, "Análise de Entregas - SLA")
    
    # Adiciona os resultados ao PDF
    c.setFont("Helvetica-Bold", 12)
    
    # Atraso por Estado
    c.drawString(50, 700, "Análises por Estado:")

    # Adiciona os resultados ao PDF
    c.setFont("Helvetica", 12)
    for i, estado in enumerate(atraso_por_estado.index):
        # Filtra o dataframe para obter todas as entregas no estado atual
        entregas_estado = df[df['Estado'] == estado]
        
        # Calcula o número total de entregas no estado
        total_entregas = entregas_estado.shape[0]
        
        # Calcula o número de entregas atrasadas e no prazo
        entregas_atrasadas = entregas_estado[entregas_estado['Dias para Entrega'] > entregas_estado['Prazo para Entrega']].shape[0]
        entregas_no_prazo = total_entregas - entregas_atrasadas
        
        # Calcula a porcentagem de qualidade
        percentual_qualidade = (entregas_no_prazo / total_entregas) * 100
        
        # Formata o texto com as informações desejadas
        text = f"{estado}: {total_entregas} entregas - {entregas_atrasadas} atrasadas - {entregas_no_prazo} no prazo - {percentual_qualidade:.2f}% de qualidade"
        
        c.drawString(50, 680 - i * 25, text)


    # Criamos nova página
    c.showPage()

    
    # Atraso por Região
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 700, "Análises por Região:")
    c.setFont("Helvetica", 12)
    
    for i, regiao in enumerate(atraso_por_regiao.index):
        # Filtra o dataframe para obter todas as entregas na região atual
        entregas_regiao = df[df['Região'] == regiao]

        # Calcula o número total de entregas na região
        total_entregas_regiao = entregas_regiao.shape[0]

        # Calcula o número de entregas atrasadas e no prazo
        entregas_atrasadas_regiao = entregas_regiao[entregas_regiao['Dias para Entrega'] > entregas_regiao['Prazo para Entrega']].shape[0]
        entregas_no_prazo_regiao = total_entregas_regiao - entregas_atrasadas_regiao

        # Calcula a porcentagem de qualidade
        percentual_qualidade_regiao = (entregas_no_prazo_regiao / total_entregas_regiao) * 100

        # Formata o texto com as informações desejadas
        text_regiao = f"{regiao}: {total_entregas_regiao} entregas - {entregas_atrasadas_regiao} atrasadas - {entregas_no_prazo_regiao} no prazo - {percentual_qualidade_regiao:.2f}% de qualidade"
        
        c.drawString(50, 660 - i * 25, text_regiao)


    # Total de Entregas dentro do Prazo
    c.drawString(50, 120, f"Total De Entregas Dentro do Prazo: {total_entrega_dentro_prazo}")

    # Total de Entregas fora do Prazo
    c.drawString(50, 100, f"Total De Entregas Fora do Prazo: {total_entrega_fora_prazo}")
    
    # Estado com Maior Percentual de Atraso
    #c.drawString(50, 120, f"Atraso por Estado %:     Maior: {estado_maior_percentual_atraso}   ||     Menor: {estado_menor_percentual_atraso}")
    
    # Cidade com Maior Percentual de Atraso
    #c.drawString(50, 100, f"Atraso por Cidade %:     Maior: {cidade_maior_percentual_atraso}   ||     Menor: {cidade_menor_percentual_atraso}")
    
    c.setFont("Helvetica-Bold", 12)            
    # Percentual de Qualidade de Entrega
    c.drawString(50, 80, f"Percentual Total de Qualidade de Entrega: {percentual_qualidade_entrega:.2f}%")
    
    
    
    # Criamos nova página
    c.showPage()

    # Análise por Transportadora
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 700, "Análises por Transportadoras:")
    c.setFont("Helvetica", 12)
    
    for i, transportadora in enumerate(atraso_por_transportadora.index):
        # Filtra o dataframe para obter todas as entregas na transportadora atual
        entregas_transportadora = df[df['Transportadora'] == transportadora]

        # Calcula o número total de entregas na transportadora
        total_entregas_transportadora = entregas_transportadora.shape[0]

        # Calcula o número de entregas atrasadas e no prazo
        entregas_atrasadas_transportadora = entregas_transportadora[entregas_transportadora['Dias para Entrega'] > entregas_transportadora['Prazo para Entrega']].shape[0]
        entregas_no_prazo_transportadora = total_entregas_transportadora - entregas_atrasadas_transportadora

        # Calcula a porcentagem de qualidade
        if total_entregas_transportadora > 0:
            percentual_qualidade_transportadora = (entregas_no_prazo_transportadora / total_entregas_transportadora) * 100
        else:
            percentual_qualidade_transportadora = 0

        # Formata o texto com as informações desejadas
        text_transportadora = f"{transportadora}: {total_entregas_transportadora} entregas - {entregas_atrasadas_transportadora} atrasadas - {entregas_no_prazo_transportadora} no prazo - {percentual_qualidade_transportadora:.2f}% de qualidade"
        
        c.drawString(50, 660 - i * 20, text_transportadora)


    # Calcula o número de estados
    #num_estados = len(atraso_por_estado)
    
    
    # Salva o arquivo PDF
    c.save()
    print(f"O arquivo {filename} foi gerado com sucesso.")



# Chama a função para criar o PDF
create_pdf(atraso_por_estado, total_entrega_dentro_prazo, total_entrega_fora_prazo, estado_maior_percentual_atraso,
           estado_menor_percentual_atraso, cidade_maior_percentual_atraso, cidade_menor_percentual_atraso, regiao_maior_percentual_atraso, 
           regiao_menor_percentual_atraso, atraso_por_regiao, atraso_por_transportadora, percentual_qualidade_entrega)