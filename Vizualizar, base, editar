# ---------- FUNÇÕES BASE ----------
def carregar_clientes():
    tabela.delete(*tabela.get_children())
    for c in banco.listar_clientes():
        tabela.insert("", tk.END, values=c)

def cliente_selecionado():
    item = tabela.focus()
    if not item:
        messagebox.showwarning("Atenção", "Selecione um cliente.")
        return None
    return tabela.item(item)["values"]

# ---------- VISUALIZAR ----------
def visualizar():
    c = cliente_selecionado()
    if not c:
        return

    cliente = banco.buscar_cliente(c[0])
    telefones = banco.listar_telefones(c[0])

    tela = tk.Toplevel(janela)
    tela.title("Visualizar Cliente")
    tela.geometry("500x550")

    labels = [
        "ID", "Nome", "Idade", "CPF", "Email",
        "Endereço", "Cidade/UF", "Nascimento", "Status"
    ]

    for i, texto in enumerate(labels):
        valor = cliente[i] if i < 8 else ("Ativo" if cliente[8] else "Inativo")
        tk.Label(tela, text=f"{texto}:",
                 font=("Arial",10,"bold")).grid(row=i, column=0, sticky="w", padx=10)
        tk.Label(tela, text=valor).grid(row=i, column=1, sticky="w")

    tk.Label(tela, text="Telefones:",
             font=("Arial",10,"bold")).grid(row=9, column=0, pady=10, padx=10)

    lista = tk.Listbox(tela, width=40)
    lista.grid(row=10, column=0, columnspan=2)
    for n, t in telefones:
        lista.insert(tk.END, f"{n} ({t})")

# ---------- ADICIONAR / EDITAR ----------
def tela_cliente(cliente_id=None):
    editar = cliente_id is not None
    dados = banco.buscar_cliente(cliente_id) if editar else None
    telefones_db = banco.listar_telefones(cliente_id) if editar else []

    tela = tk.Toplevel(janela)
    tela.title("Editar Cliente" if editar else "Adicionar Cliente")
    tela.geometry("550x650")

    campos = {}
    nomes = [
        "Nome", "Idade", "CPF", "Email",
        "Endereço", "Cidade/UF", "Nascimento"
    ]

    for i, nome in enumerate(nomes):
        tk.Label(tela, text=nome).grid(row=i, column=0, padx=10, sticky="w")
        e = tk.Entry(tela, width=40)
        if editar:
            e.insert(0, dados[i+1])
        e.grid(row=i, column=1)
        campos[nome] = e

    status = tk.IntVar(value=dados[8] if editar else 1)
    tk.Checkbutton(tela, text="Ativo", variable=status)\
        .grid(row=7, column=1, sticky="w")
