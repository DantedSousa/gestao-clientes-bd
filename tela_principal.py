# ---------- TELEFONES ----------
    tk.Label(tela, text="Telefones", font=("Arial",10,"bold"))\
        .grid(row=8, column=0, pady=10)

    lista = tk.Listbox(tela, width=45)
    lista.grid(row=9, column=0, columnspan=2, padx=10)

    telefones = []
    for n, t in telefones_db:
        telefones.append([n, t])
        lista.insert(tk.END, f"{n} ({t})")

    ent_num = tk.Entry(tela)
    ent_num.grid(row=10, column=0, padx=10)

    combo = ttk.Combobox(
        tela,
        values=["Celular", "Fixo", "WhatsApp"],
        state="readonly"
    )
    combo.current(0)
    combo.grid(row=10, column=1, padx=10)

    def add_tel():
        numero = ent_num.get().strip()
        tipo = combo.get().strip()

        if not numero:
            messagebox.showwarning("Erro", "Digite o número do telefone.")
            return

        telefones.append([numero, tipo])
        lista.insert(tk.END, f"{numero} ({tipo})")
        ent_num.delete(0, tk.END)
        combo.current(0)

    def sel_tel(_):
        i = lista.curselection()
        if i:
            ent_num.delete(0, tk.END)
            ent_num.insert(0, telefones[i[0]][0])
            combo.set(telefones[i[0]][1])

    def upd_tel():
        i = lista.curselection()
        if i:
            telefones[i[0]] = [ent_num.get(), combo.get()]
            lista.delete(i)
            lista.insert(i, f"{ent_num.get()} ({combo.get()})")

    def del_tel():
        i = lista.curselection()
        if i:
            telefones.pop(i[0])
            lista.delete(i)

    lista.bind("<<ListboxSelect>>", sel_tel)

    tk.Button(tela, text="Adicionar", command=add_tel).grid(row=11, column=0, pady=5)
    tk.Button(tela, text="Atualizar", command=upd_tel).grid(row=11, column=1, pady=5)
    tk.Button(tela, text="Remover", command=del_tel).grid(row=11, column=2, pady=5)

    def salvar():
        dados_cliente = (
            campos["Nome"].get(),
            int(campos["Idade"].get() or 0),
            campos["CPF"].get(),
            campos["Email"].get(),
            campos["Endereço"].get(),
            campos["Cidade/UF"].get(),
            campos["Nascimento"].get(),
            status.get()
        )

        if editar:
            banco.atualizar_cliente(cliente_id, dados_cliente)
            banco.remover_telefones(cliente_id)
            banco.inserir_telefones(cliente_id, telefones)
        else:
            novo_id = banco.inserir_cliente(dados_cliente)
            banco.inserir_telefones(novo_id, telefones)

        carregar_clientes()
        tela.destroy()
        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")

    tk.Button(tela, text="Salvar", width=20, command=salvar)\
        .grid(row=12, column=0, columnspan=2, pady=20)

# ---------- DELETAR ----------
def deletar():
    c = cliente_selecionado()
    if not c:
        return
    if messagebox.askyesno("Confirmar", "Deseja excluir este cliente?"):
        banco.deletar_cliente(c[0])
        carregar_clientes()

# ---------- JANELA PRINCIPAL ----------
janela = tk.Tk()
janela.title("Gestão de Clientes")
janela.geometry("800x500")

tk.Label(janela, text="Clientes", font=("Arial",16,"bold")).pack(pady=10)

tabela = ttk.Treeview(janela, columns=("id","nome","cpf","email"), show="headings")
for c in ("id","nome","cpf","email"):
    tabela.heading(c, text=c.upper())
tabela.pack(expand=True, fill="both", padx=10)

frame = tk.Frame(janela)
frame.pack(pady=15)

tk.Button(frame, text="Visualizar", width=15, command=visualizar).grid(row=0,column=0,padx=5)
tk.Button(frame, text="Adicionar", width=15, command=lambda: tela_cliente()).grid(row=0,column=1,padx=5)
tk.Button(frame, text="Editar", width=15,
          command=lambda: tela_cliente(cliente_selecionado()[0])).grid(row=0,column=2,padx=5)
tk.Button(frame, text="Deletar", width=15, command=deletar).grid(row=0,column=3,padx=5)

carregar_clientes()
janela.mainloop()

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