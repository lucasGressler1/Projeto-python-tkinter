import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import random
import sqlite3

class BancoDeDados:
    def __init__(self, nome_arquivo):
        self.conexao = sqlite3.connect(nome_arquivo)
        self.cursor = self.conexao.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS filmes (
            titulo TEXT,
            diretor TEXT,
            ano INTEGER
        )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS comidas (
            comida TEXT,
            bebida TEXT
        )""")
        self.conexao.commit()

    def inserir_filme(self, filme):
        self.cursor.execute("INSERT INTO filmes VALUES (?, ?, ?)", (filme.titulo, filme.diretor, filme.ano))
        self.conexao.commit()

    def inserir_comida(self, comida):
        self.cursor.execute("INSERT INTO comidas VALUES (?, ?)", (comida.comida, comida.bebida))
        self.conexao.commit()

    def listar_filmes(self):
        self.cursor.execute("SELECT * FROM filmes")
        return self.cursor.fetchall()

    def listar_comidas(self):
        self.cursor.execute("SELECT * FROM comidas")
        return self.cursor.fetchall()

    def excluir_filme(self, titulo):
        self.cursor.execute("DELETE FROM filmes WHERE titulo=?", (titulo,))
        self.conexao.commit()

    def excluir_comida(self, comida, bebida):
        self.cursor.execute("DELETE FROM comidas WHERE comida=? AND bebida=?", (comida, bebida))
        self.conexao.commit()

class Filme:
    def __init__(self, titulo, diretor, ano):
        self.titulo = titulo
        self.diretor = diretor
        self.ano = ano

class Comida:
    def __init__(self, comida, bebida):
        self.comida = comida
        self.bebida = bebida

class Aplicacao:
    def __init__(self, master):
        self.bd = BancoDeDados("filmes.db")
        self.master = master
        master.title("Filmes e Comidas")
        master.resizable(False, False)
        # master.configure(bg="black")  # Set background color to black

        # Estilo
        style = ttk.Style()
        style.theme_use('clam')  # seleciona o tema "clam"
        
         # BACKGROUND DA TELA INTEIRA
        
        style.configure('TFrame', borderwidth=5, relief='ridge', background='black')
    
        style.configure('Tdelete', background='black', foreground='white')
        style.configure('TLabel', background='black', foreground='white')
        style.configure('TButton', background='black', foreground='white')
        style.configure('Treeview', background='black', foreground='white')
        style.map('Treeview', background=[('selected', 'green')])


        # Frame principal
        self.frame_principal = ttk.Frame(master)
        self.frame_principal.grid(row=0, column=0, padx=10, pady=10)

        # LabelFrame de Cadastro de Filmes
        self.labelframe_cadastro_filmes = ttk.LabelFrame(self.frame_principal, text=" Cadastro de Filmes ")
        self.labelframe_cadastro_filmes.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Label e Entry para o título do filme
        self.label_titulo = ttk.Label(self.labelframe_cadastro_filmes, text="Título:")
        self.label_titulo.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_titulo = ttk.Entry(self.labelframe_cadastro_filmes, width=30)
        self.entry_titulo.grid(row=0, column=1, padx=5, pady=5)

        # Label e Entry para o diretor do filme
        self.label_diretor = ttk.Label(self.labelframe_cadastro_filmes, text="Diretor:")
        self.label_diretor.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_diretor = ttk.Entry(self.labelframe_cadastro_filmes, width=30)
        self.entry_diretor.grid(row=1, column=1, padx=5, pady=5)

        # Label e Entry para o ano do filme
        self.label_ano = ttk.Label(self.labelframe_cadastro_filmes, text="Ano:")
        self.label_ano.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_ano = ttk.Entry(self.labelframe_cadastro_filmes, width=10)
        self.entry_ano.grid(row=2, column=1, padx=5, pady=5)

        # Botão para cadastrar o filme
        self.button_cadastrar_filme = ttk.Button(self.labelframe_cadastro_filmes, text="Cadastrar Filme", command=self.cadastrar_filme)
        self.button_cadastrar_filme.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        # LabelFrame de Cadastro de Comidas
        self.labelframe_cadastro_comidas = ttk.LabelFrame(self.frame_principal, text=" Cadastro de Comidas ")
        self.labelframe_cadastro_comidas.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Label e Entry para o nome da comida
        self.label_comida = ttk.Label(self.labelframe_cadastro_comidas, text="Comida:")
        self.label_comida.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_comida = ttk.Entry(self.labelframe_cadastro_comidas, width=30)
        self.entry_comida.grid(row=0, column=1, padx=5, pady=5)

         # Label e Entry para o nome da comida
        self.label_bebida = ttk.Label(self.labelframe_cadastro_comidas, text="Bebidas:")
        self.label_bebida.grid(row=2, column=0, padx=5, pady=10, sticky="w")
        self.entry_bebida = ttk.Entry(self.labelframe_cadastro_comidas, width=30)
        self.entry_bebida.grid(row=2, column=1, padx=5, pady=10)

        # Botão para cadastrar a comida
        self.button_cadastrar_comida = ttk.Button(self.labelframe_cadastro_comidas, text="Cadastrar Comida", command=self.cadastrar_comida)
        self.button_cadastrar_comida.grid(row=3, column=1, columnspan=2, padx=0, pady=5)

        # LabelFrame de Listagem de Filmes
        self.labelframe_listagem_filmes = ttk.LabelFrame(self.frame_principal, text=" Listagem de Filmes ")
        self.labelframe_listagem_filmes.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Treeview para exibir a lista de filmes
        self.treeview_filmes = ttk.Treeview(self.labelframe_listagem_filmes, columns=("Diretor", "Ano"))
        self.treeview_filmes.column("#0", width=200)
        self.treeview_filmes.column("Diretor", width=150)
        self.treeview_filmes.column("Ano", width=50)
        self.treeview_filmes.heading("#0", text="Título")
        self.treeview_filmes.heading("Diretor", text="Diretor")
        self.treeview_filmes.heading("Ano", text="Ano")
        self.treeview_filmes.grid(row=0, column=0, sticky="nsew")

        # LabelFrame de Listagem de Comidas
        self.labelframe_listagem_comidas = ttk.LabelFrame(self.frame_principal, text=" Listagem de Comidas ")
        self.labelframe_listagem_comidas.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Treeview para exibir a lista de comidas
        self.treeview_comidas = ttk.Treeview(self.labelframe_listagem_comidas, columns=("Comida"))
        self.treeview_comidas.column("#0", width=200)
        self.treeview_comidas.heading("#0", text="Comida")
        self.treeview_comidas.heading("#1", text="Bebida")

        self.treeview_comidas.grid(row=0, column=0, sticky="nsew")

        # Botão para atualizar a lista de filmes
        self.button_atualizar_filmes = ttk.Button(self.labelframe_listagem_filmes, text="Atualizar Filmes", command=self.listar_filmes)
        self.button_atualizar_filmes.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Botão para atualizar a lista de comidas
        self.button_atualizar_comidas = ttk.Button(self.labelframe_listagem_comidas, text="Atualizar Comidas", command=self.listar_comidas)
        self.button_atualizar_comidas.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Botão para sortear filme e comida
        self.button_sortear = ttk.Button(self.frame_principal, text="Sortear", command=self.sortear_filme_comida)
        self.button_sortear.grid(row=2, column=0, columnspan=1, padx=40, pady=20)

        
        # Botão para Deletar
        self.button_delete = ttk.Button(self.frame_principal, text="Deletar", command=self.excluir_selecionado)
        self.button_delete.grid(row=2, column=1, columnspan=2, padx=0, pady=20)


        # Estilo para os botões
        style.configure('TButton', font=('Arial', 12), foreground='white', background='black', width=20)
        self.button_cadastrar_filme.configure(style='TButton')
        self.button_cadastrar_comida.configure(style='TButton')
        self.button_atualizar_filmes.configure(style='TButton')
        self.button_atualizar_comidas.configure(style='TButton')
        self.button_sortear.configure(style='TButton')
        self.button_delete.configure(style='TButton')

        # Estilo para os labels e entries
        style.configure('TLabel', font=('Arial', 12), background='grey', foreground='white')
        style.configure('TEntry', font=('Arial', 12))

        # Estilo para os labelframes
        style.configure('TLabelframe.Label', font=('Arial', 14, 'bold'), foreground='black', background='transparent')

        # Estilo para os treeviews
        style.configure('Treeview', font=('Arial', 12))
        style.configure('Treeview.Heading', font=('Arial', 12, 'bold'))

        # Configuração das proporções de redimensionamento
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)
        master.rowconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)
        self.labelframe_cadastro_filmes.columnconfigure(0, weight=1)
        self.labelframe_cadastro_filmes.columnconfigure(1, weight=1)
        self.labelframe_cadastro_comidas.columnconfigure(0, weight=1)
        self.labelframe_cadastro_comidas.columnconfigure(1, weight=1)
        self.labelframe_listagem_filmes.rowconfigure(0, weight=1)
        self.labelframe_listagem_filmes.columnconfigure(0, weight=1)
        self.labelframe_listagem_comidas.rowconfigure(0, weight=1)
        self.labelframe_listagem_comidas.columnconfigure(0, weight=1)
        self.frame_principal.rowconfigure(0, weight=1)
        self.frame_principal.rowconfigure(1, weight=1)
        self.frame_principal.columnconfigure(0, weight=1)
        self.frame_principal.columnconfigure(1, weight=1)

        # Configuração do tamanho do widget
        master.geometry("850x600")

    def cadastrar_filme(self):
        titulo = self.entry_titulo.get()
        diretor = self.entry_diretor.get()
        ano = self.entry_ano.get()

        if titulo and diretor and ano:
            filme = Filme(titulo, diretor, ano)
            self.bd.inserir_filme(filme)
            self.listar_filmes()
            self.entry_titulo.delete(0, tk.END)
            self.entry_diretor.delete(0, tk.END)
            self.entry_ano.delete(0, tk.END)
        else:
            tk.messagebox.showwarning("Aviso", "Preencha todos os campos!")

    def cadastrar_comida(self):
        comida = self.entry_comida.get()
        bebida = self.entry_bebida.get()

        if comida and bebida:
            comida = Comida(comida, bebida)
            self.bd.inserir_comida(comida)
            self.listar_comidas()
    
            self.entry_bebida.delete(0, tk.END)
            self.entry_comida.delete(0, tk.END)
        else:
            tk.messagebox.showwarning("Aviso", "Preencha o campo!")

    def listar_filmes(self):
        self.treeview_filmes.delete(*self.treeview_filmes.get_children())
        filmes = self.bd.listar_filmes()
        for filme in filmes:
            self.treeview_filmes.insert("", tk.END, text=filme[0], values=(filme[1], filme[2]))

    def listar_comidas(self):
        self.treeview_comidas.delete(*self.treeview_comidas.get_children())
        comidas = self.bd.listar_comidas()
        for comida in comidas:
            self.treeview_comidas.insert("", tk.END, text=comida[0], values=(comida[1]) )

    def excluir_selecionado(self):
        item_filme_selecionado = self.treeview_filmes.selection()
        item_comida_selecionado = self.treeview_comidas.selection()

        if item_filme_selecionado:
            for item in item_filme_selecionado:
                filme_selecionado = self.treeview_filmes.item(item)
                titulo = filme_selecionado["text"]
                self.bd.excluir_filme(titulo)
            self.listar_filmes()

        if item_comida_selecionado:
            for item in item_comida_selecionado:
                comida_selecionada = self.treeview_comidas.item(item)
                comida = comida_selecionada["text"]
                bebida = comida_selecionada["values"][0]
                self.bd.excluir_comida(comida, bebida)
            self.listar_comidas()


    def sortear_filme_comida(self):
        filmes = self.bd.listar_filmes()
        comidas = self.bd.listar_comidas()


        if not filmes or not comidas:
            tk.messagebox.showwarning("Aviso", "Não há filmes ou comidas cadastrados!")
            return

        filme_sorteado = random.choice(filmes)
        comida_sorteada = random.choice(comidas)

        tk.messagebox.showinfo("Sorteio", f"Filme Sorteado: {filme_sorteado[0]}\nComida Sorteada: {comida_sorteada[0], comida_sorteada[1]}")

root = tk.Tk()
app = Aplicacao(root)
root.mainloop()