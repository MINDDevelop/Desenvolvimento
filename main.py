from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors

# Nome do arquivo PDF de saída
filename = 'relatorio.pdf'

# Criar um documento básico
doc = SimpleDocTemplate(filename, pagesize=letter)

# Contentor para os elementos do PDF
elements = []

# Título do Relatório
elements.append(Spacer(1, 12))
title = 'Relatório 09/04/2024'
elements.append(Table([[title]], style=[('ALIGN', (0,0), (0,0), 'CENTER')]))

# Seção de Principais Notícias
elements.append(Spacer(1, 12))
news_title = 'PRINCIPAIS NOTÍCIAS'
elements.append(Table([[news_title]], style=[('ALIGN', (0,0), (0,0), 'LEFT')]))
# Adicione aqui as notícias

# Seção de TRADE IDEAS
elements.append(Spacer(1, 24))
trade_ideas_title = 'TRADE IDEAS'
elements.append(Table([[trade_ideas_title]], style=[('ALIGN', (0,0), (0,0), 'LEFT')]))

# Tabela de trade ideas
data = [
    ['HORÁRIO', 'OPERAÇÃO', 'TICKER', 'VENCIMENTO', 'STRIKE', 'DIAS ÚTEIS', 'ROA (%)', 'PREÇO', '#DIV/0! QUANTIDADE'],
    # Adicione aqui os dados da sua tabela...
]

table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
elements.append(table)

# Construir o PDF
doc.build(elements)

print(f"PDF criado: {filename}")