import mysql.connector

# ---------- CONEXÃO ----------
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="carlos.dante08",
        database="gestao_clientes"
    )

# ---------- CLIENTES ----------
def listar_clientes():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, nome, cpf, email FROM clientes")
    dados = cur.fetchall()
    cur.close()
    con.close()
    return dados

def buscar_cliente(cliente_id):
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        SELECT id, nome, idade, cpf, email, endereco,
               localidade, data_nascimento, status
        FROM clientes WHERE id=%s
    """, (cliente_id,))
    cliente = cur.fetchone()
    cur.close()
    con.close()
    return cliente

def inserir_cliente(dados):
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        INSERT INTO clientes
        (nome, idade, cpf, email, endereco, localidade, data_nascimento, status)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, dados)
    con.commit()
    cliente_id = cur.lastrowid
    cur.close()
    con.close()
    return cliente_id

def atualizar_cliente(cliente_id, dados):
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        UPDATE clientes SET
        nome=%s, idade=%s, cpf=%s, email=%s,
        endereco=%s, localidade=%s,
        data_nascimento=%s, status=%s
        WHERE id=%s
    """, (*dados, cliente_id))
    con.commit()
    cur.close()
    con.close()

def deletar_cliente(cliente_id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM clientes WHERE id=%s", (cliente_id,))
    con.commit()
    cur.close()
    con.close()

# ---------- TELEFONES ----------
def listar_telefones(cliente_id):
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        SELECT numero, tipo
        FROM cliente_telefones
        WHERE clientes_id=%s
    """, (cliente_id,))
    telefones = cur.fetchall()
    cur.close()
    con.close()
    return telefones

def remover_telefones(cliente_id):
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "DELETE FROM cliente_telefones WHERE clientes_id=%s",
        (cliente_id,)
    )
    con.commit()
    cur.close()
    con.close()

def inserir_telefones(cliente_id, telefones):
    con = conectar()
    cur = con.cursor()
    for numero, tipo in telefones:
        cur.execute("""
            INSERT INTO cliente_telefones (numero, tipo, clientes_id)
            VALUES (%s,%s,%s)
        """, (numero, tipo, cliente_id))
    con.commit()
    cur.close()
    con.close()
