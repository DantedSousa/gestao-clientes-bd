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
