import pyodbc

server = 'tcp:dbmind.database.windows.net,1433'
database = 'DBMIND'
username = 'vgoncalves@mindinc.com.br'
authentication = 'ActiveDirectoryIntegrated'

# Construindo a string de conexão
conn_str = (
    'Driver={ODBC Driver 18 for SQL Server};'
    f'Server={server};'
    f'Database={database};'
    f'Uid={username};'
    'Encrypt=yes;'
    'TrustServerCertificate=no;'
    'Connection Timeout=30;'
    f'Authentication={authentication}'
)
try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Exemplo de consulta
    cursor.execute('SELECT @@version;')
    row = cursor.fetchone()
    while row:
        print(row[0])
        row = cursor.fetchone()

    cursor.close()
    conn.close()
except Exception as e:
    print("Erro ao conectar ao banco de dados:", e)