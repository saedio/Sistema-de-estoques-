import sqlite3


conn = sqlite3.connect('farmacia.db')
cursor = conn.cursor()

# Criar tabela produtos se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE,
    estoque INTEGER
)
''')
conn.commit()

#funções de adicionar, atualizar, mostrar
def adicionar_remedio(nome, quantidade):
    try:
        cursor.execute('INSERT INTO produtos (nome, estoque) VALUES (?, ?)', (nome, quantidade))
        conn.commit()
        print(f"{nome} adicionado com estoque {quantidade}.")
    except sqlite3.IntegrityError:
        print(f"{nome} já existe no banco de dados.")

def atualizar_estoque(nome, quantidade):
    cursor.execute('SELECT estoque FROM produtos WHERE nome = ?', (nome,))
    result = cursor.fetchone()
    if result:
        novo_estoque = result[0] + quantidade
        cursor.execute('UPDATE produtos SET estoque = ? WHERE nome = ?', (novo_estoque, nome))
        conn.commit()
        print(f"Estoque de {nome} atualizado para {novo_estoque}.")
    else:
        print(f"{nome} não encontrado no banco de dados.")

def mostrar_estoque():
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    print("\nEstoque Atual:")
    for p in produtos:
        print(f"ID: {p[0]}, Produto: {p[1]}, Estoque: {p[2]}")
    print("")

# Lista inicial de remédios
lista_remedios = [
    ("Paracetamol", 50),
    ("Ibuprofeno", 30),
    ("Amoxicilina", 20)
]

# Adicionar remédios
for remedio, qtd in lista_remedios:
    adicionar_remedio(remedio, qtd)

# Testes de atualização
atualizar_estoque("Paracetamol", 10)
atualizar_estoque("Ibuprofeno", -5)

# Mostrar estoque final
mostrar_estoque()

# Fechar conexão
conn.close()
