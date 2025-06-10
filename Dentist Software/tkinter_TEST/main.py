import tkinter as tk
from tkinter import messagebox, ttk, PhotoImage, font
import csv
from datetime import datetime, timedelta
from tkcalendar import Calendar
from tkinter import filedialog
import os
import shutil

# Definição de cores e estilos
AZUL_CLARO = "#4BA3C3"
BRANCO = "#FFFFFF"
CINZA_CLARO = "#F5F5F5"
CINZA_ESCURO = "#4A4A4A"
VERDE_MENTA = "#A7D7C5"

FONTE_TITULO = ("Montserrat", 16, "bold")
FONTE_CORPO = ("Lato", 10)
FONTE_DESTAQUE = ("Roboto", 12)

# Função para aplicar estilo aos widgets
def aplicar_estilo(widget):
    if isinstance(widget, tk.Tk) or isinstance(widget, tk.Toplevel):
        widget.configure(bg=BRANCO)
    elif isinstance(widget, tk.Frame):
        widget.configure(bg=BRANCO)
    elif isinstance(widget, tk.Label):
        widget.configure(bg=BRANCO, fg=CINZA_ESCURO, font=FONTE_CORPO)
    elif isinstance(widget, tk.Button):
        widget.configure(bg=AZUL_CLARO, fg=BRANCO, font=FONTE_DESTAQUE, relief=tk.FLAT, bd=0, padx=10, pady=5)
        widget.bind("<Enter>", lambda e: e.widget.configure(bg=VERDE_MENTA))
        widget.bind("<Leave>", lambda e: e.widget.configure(bg=AZUL_CLARO))
    elif isinstance(widget, tk.Entry):
        widget.configure(font=FONTE_CORPO, relief=tk.FLAT, bd=1, bg=CINZA_CLARO)
    elif isinstance(widget, ttk.Combobox):
        widget.configure(font=FONTE_CORPO)

    for child in widget.winfo_children():
        aplicar_estilo(child)

usuarios_lista = ['','g']
senha_lista = ['', '1']
# Função para verificar login
def verificar_login():
    usuario = usuario_entry.get()
    senha = senha_entry.get()
    
    if usuario in usuarios_lista and senha == senha_lista[usuarios_lista.index(usuario)]:
        #messagebox.showinfo("Sucesso", "Login bem-sucedido!")
        abrir_pagina_principal()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos!")

# Função para abrir a página principal
def abrir_pagina_principal():
    login_janela.destroy()
    global root
    root = tk.Tk()
    root.title("Clínica Odontológica Flávinho")
    root.geometry("500x400")
    # Título
    titulo = tk.Label(root, text="Clínica Odontológica - Flavinho ", font=('arial', 20, 'bold'))
    titulo.pack(pady=20)

    botoes_frame = tk.Frame(root)
    botoes_frame.pack(pady=20)

    botoes = [
        ("Cadastro de Paciente", abrir_pagina_cadastro),
        ("Lista de Materiais", abrir_lista_materiais),
        ("Upload de Exames", abrir_upload_exames),
        ("Agendar Consulta", abrir_agendar_consulta),
        ("Consultar pacientes", abrir_analise_de_pacientes)
    ]

    for texto, comando in botoes:
        btn = tk.Button(botoes_frame, text=texto, command=comando, width=20)
        btn.pack(pady=10)

    aplicar_estilo(root)

# Função para abrir a página de agendar consultas
def abrir_agendar_consulta():
    agendar_janela = tk.Toplevel(root)
    agendar_janela.title("Agendar Consulta")

    tk.Label(agendar_janela, text="Selecione o Paciente:").pack(pady=10)

    # Criação da lista de pacientes
    pacientes = []
    with open('pacientes.csv', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            pacientes.append(row[0])  # Adiciona apenas o nome do paciente à lista

    paciente_combobox = ttk.Combobox(agendar_janela, values=pacientes)
    paciente_combobox.pack(pady=5)

    # Tipos de consultas/procedimentos pré-definidos
    tipos_consulta = {
        "Limpeza": {"Pasta de polimento": 10, "Fio dental": 1},
        "Extração": {"Anestesia": 5, "Gaze": 5},
        "Restauração": {"Resina": 2, "Anestesia": 3},
        "Clareamento": {"Gel clareador": 15},
        "Aplicação de flúor": {"Flúor gel": 5},
        "Tratamento de canal": {"Anestesia": 5, "Guta-percha": 1}
    }

    tk.Label(agendar_janela, text="Tipo de Consulta:").pack(pady=10)
    tipo_combobox = ttk.Combobox(agendar_janela, values=list(tipos_consulta.keys()))
    tipo_combobox.pack(pady=5)

    tk.Label(agendar_janela, text="Selecione a data da consulta:").pack(pady=10)

    # Criação do calendário
    calendario = Calendar(agendar_janela, selectmode='day')
    calendario.pack(pady=10)

    def agendar():
        paciente_selecionado = paciente_combobox.get()
        tipo_consulta = tipo_combobox.get()
        data_selecionada = calendario.get_date()

        if paciente_selecionado and tipo_consulta:
            # Registrar a consulta
            with open('consultas.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([paciente_selecionado, tipo_consulta, data_selecionada])

            # Atualizar a planilha de materiais
            materiais_necessarios = tipos_consulta[tipo_consulta]
            atualizar_materiais(materiais_necessarios)

            messagebox.showinfo("Sucesso", f"Consulta agendada para {paciente_selecionado} em {data_selecionada} com tipo '{tipo_consulta}'.")
            agendar_janela.destroy()
        else:
            messagebox.showwarning("Erro", "Por favor, selecione um paciente e um tipo de consulta.")
    
    tk.Button(agendar_janela, text="Agendar Consulta", command=agendar).pack(pady=10)

def atualizar_materiais(materiais_necessarios):
    try:
        with open('materiais.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            materiais = list(reader)
    except FileNotFoundError:
        materiais = []

    for material, quantidade in materiais_necessarios.items():
        material_encontrado = False
        for row in materiais:
            if row[1] == material:
                nova_quantidade = int(row[2]) - quantidade
                row[2] = str(nova_quantidade)
                if nova_quantidade <= 10: 
                    row[3] = "Sim"
                material_encontrado = True
                break
        
        if not material_encontrado:
            novo_id = len(materiais) + 1
            materiais.append([novo_id, material, str(-quantidade), "Sim"])

    with open('materiais.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(materiais)

# Função para abrir a página de cadastro de paciente
def abrir_pagina_cadastro():
    cadastro_janela = tk.Toplevel(root)
    cadastro_janela.title("Cadastro de Paciente")
    cadastro_janela.geometry('300x150')
    
    tk.Label(cadastro_janela, text="Nome do Paciente", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
    nome_entry = tk.Entry(cadastro_janela, font=("Arial", 10))
    nome_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(cadastro_janela, text="Idade", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
    idade_entry = tk.Entry(cadastro_janela, font=("Arial", 10))
    idade_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(cadastro_janela, text="CPF", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=5, pady=5)
    cpf_entry = tk.Entry(cadastro_janela, font=("Arial", 10))
    cpf_entry.grid(row=2, column=1, padx=5, pady=5)

    def salvar_paciente():
        nome = nome_entry.get()
        idade = idade_entry.get()
        cpf = cpf_entry.get()
        
        if nome and idade and cpf:
            with open('pacientes.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([nome, idade, cpf])
                messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")
                cadastro_janela.destroy()
        else:
            messagebox.showwarning("Erro", "Todos os campos são obrigatórios!")
    
    tk.Button(cadastro_janela, text="Salvar", command=salvar_paciente).grid(row=3, columnspan=2)

def abrir_lista_materiais():
    materiais_janela = tk.Toplevel(root)
    materiais_janela.title("Lista de Materiais")
    materiais_janela.geometry('400x600')

    try:
        with open('materiais.csv', newline='') as file:
            reader = csv.reader(file)
            materiais = list(reader)
    except FileNotFoundError:
        materiais = []

    # Frame para a lista de materiais
    lista_frame = tk.Frame(materiais_janela)
    lista_frame.pack(pady=10)

    # Criação da Treeview para exibir os materiais
    colunas = ('ID', 'Nome do Material', 'Quantidade', 'Precisa Comprar')
    tree = ttk.Treeview(lista_frame, columns=colunas, show='headings')

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    for material in materiais:
        tree.insert('', 'end', values=material)

    tree.pack(side='left', fill='y')

    # Scrollbar para a Treeview
    scrollbar = ttk.Scrollbar(lista_frame, orient='vertical', command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)

    # Frame para adicionar/editar materiais
    edit_frame = tk.Frame(materiais_janela)
    edit_frame.pack(pady=10)

    tk.Label(edit_frame, text="Nome do Material").grid(row=0, column=0)
    nome_entry = tk.Entry(edit_frame)
    nome_entry.grid(row=0, column=1)

    tk.Label(edit_frame, text="Quantidade").grid(row=1, column=0)
    quantidade_entry = tk.Entry(edit_frame)
    quantidade_entry.grid(row=1, column=1)

    precisa_comprar_var = tk.BooleanVar()
    precisa_comprar_check = tk.Checkbutton(edit_frame, text="Precisa Comprar", variable=precisa_comprar_var)
    precisa_comprar_check.grid(row=2, columnspan=2)

    def adicionar_material():
        nome = nome_entry.get()
        quantidade = quantidade_entry.get()
        precisa_comprar = "Sim" if precisa_comprar_var.get() else "Não"
        if nome and quantidade:
            novo_id = len(materiais) + 1
            novo_material = [novo_id, nome, quantidade, precisa_comprar]
            materiais.append(novo_material)
            tree.insert('', 'end', values=novo_material)
            salvar_materiais()
            nome_entry.delete(0, 'end')
            quantidade_entry.delete(0, 'end')
            precisa_comprar_var.set(False)
        else:
            messagebox.showwarning("Erro", "Preencha todos os campos!")

    def editar_material():
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            valores = item['values']
            nome_entry.delete(0, 'end')
            nome_entry.insert(0, valores[1])
            quantidade_entry.delete(0, 'end')
            quantidade_entry.insert(0, valores[2])
            precisa_comprar_var.set(valores[3] == "Sim")
            
            def salvar_edicao():
                valores[1] = nome_entry.get()
                valores[2] = quantidade_entry.get()
                valores[3] = "Sim" if precisa_comprar_var.get() else "Não"
                tree.item(selected_item, values=valores)
                salvar_materiais()
                editar_btn.config(text="Editar", command=editar_material)
            
            editar_btn.config(text="Salvar Edição", command=salvar_edicao)
        else:
            messagebox.showwarning("Erro", "Selecione um material para editar!")

    def salvar_materiais():
        with open('materiais.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for item in tree.get_children():
                writer.writerow(tree.item(item)['values'])

    adicionar_btn = tk.Button(edit_frame, text="Adicionar Material", command=adicionar_material)
    adicionar_btn.grid(row=3, column=0, pady=5)

    editar_btn = tk.Button(edit_frame, text="Editar", command=editar_material)
    editar_btn.grid(row=3, column=1, pady=5)

# Função para abrir a página de upload de exames
from tkinter import filedialog
import os
import shutil

def abrir_upload_exames():
    upload_janela = tk.Toplevel(root)
    upload_janela.title("Upload e Pesquisa de Exames (PDF)")
    upload_janela.geometry("500x400")
    aplicar_estilo(upload_janela)

    notebook = ttk.Notebook(upload_janela)
    notebook.pack(expand=True, fill='both', padx=10, pady=10)

    # Aba de Upload
    upload_frame = tk.Frame(notebook)
    notebook.add(upload_frame, text='Upload de Exames')

    tk.Label(upload_frame, text="Nome do Paciente:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    nome_entry = tk.Entry(upload_frame)
    nome_entry.grid(row=0, column=1, padx=5, pady=5)

    arquivo_selecionado = tk.StringVar()
    tk.Label(upload_frame, text="Arquivo selecionado:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    tk.Label(upload_frame, textvariable=arquivo_selecionado).grid(row=1, column=1, padx=5, pady=5)

    def selecionar_arquivo():
        filetypes = [('PDF files', '*.pdf')]
        filename = filedialog.askopenfilename(title="Selecione o arquivo PDF", filetypes=filetypes)
        if filename:
            arquivo_selecionado.set(os.path.basename(filename))
            return filename
        return None

    def fazer_upload():
        nome = nome_entry.get().strip()
        arquivo = arquivo_selecionado.get()

        if not nome or not arquivo:
            messagebox.showwarning("Erro", "Por favor, preencha o nome do paciente e selecione um arquivo.")
            return

        try:
            with open('pacientes.csv', newline='') as file:
                reader = csv.reader(file)
                encontrado = any(row[0].lower() == nome.lower() for row in reader)

            if encontrado:
                # Criar diretório de exames se não existir
                os.makedirs('exames', exist_ok=True)

                # Extrair a extensão do arquivo original
                _, extensao = os.path.splitext(arquivo)

                # Gerar o novo nome do arquivo
                data_atual = datetime.now().strftime("%Y%m%d_%H%M%S")
                tipo_exame = "Exame"  # Você pode adicionar uma entrada para o tipo de exame, se desejar
                novo_nome_arquivo = f"{nome}_{tipo_exame}_{data_atual}{extensao}"

                # Copiar o arquivo para o diretório de exames
                shutil.copy(selecionar_arquivo(), os.path.join('exames', novo_nome_arquivo))

                # Registrar o upload no CSV
                with open('exames_uploads.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([nome, novo_nome_arquivo, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

                messagebox.showinfo("Sucesso", f"Exame '{novo_nome_arquivo}' foi anexado ao paciente {nome}.")
                upload_janela.destroy()
            else:
                messagebox.showwarning("Erro", "Paciente não cadastrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao fazer o upload: {str(e)}")

    tk.Button(upload_frame, text="Selecionar Arquivo", command=selecionar_arquivo).grid(row=2, column=0, padx=5, pady=10)
    tk.Button(upload_frame, text="Fazer Upload", command=fazer_upload).grid(row=2, column=1, padx=5, pady=10)

    # Aba de Pesquisa
    pesquisa_frame = tk.Frame(notebook)
    notebook.add(pesquisa_frame, text='Pesquisar Exames')

    tk.Label(pesquisa_frame, text="Nome do Paciente:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    pesquisa_entry = tk.Entry(pesquisa_frame)
    pesquisa_entry.grid(row=0, column=1, padx=5, pady=5)

    resultados_tree = ttk.Treeview(pesquisa_frame, columns=('Nome', 'Arquivo', 'Data'), show='headings')
    resultados_tree.heading('Nome', text='Nome do Paciente')
    resultados_tree.heading('Arquivo', text='Nome do Arquivo')
    resultados_tree.heading('Data', text='Data de Upload')
    resultados_tree.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

    scrollbar = ttk.Scrollbar(pesquisa_frame, orient='vertical', command=resultados_tree.yview)
    scrollbar.grid(row=1, column=2, sticky='ns')
    resultados_tree.configure(yscrollcommand=scrollbar.set)

    def pesquisar_exames():
        nome_pesquisa = pesquisa_entry.get().strip().lower()
        resultados_tree.delete(*resultados_tree.get_children())
        
        try:
            with open('exames_uploads.csv', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if nome_pesquisa in row[0].lower():
                        resultados_tree.insert('', 'end', values=row)
        except FileNotFoundError:
            messagebox.showinfo("Informação", "Nenhum exame encontrado.")

    def abrir_exame():
        selected_item = resultados_tree.selection()
        if selected_item:
            arquivo = resultados_tree.item(selected_item)['values'][1]
            caminho_completo = os.path.join('exames', arquivo)
            if os.path.exists(caminho_completo):
                os.startfile(caminho_completo)
            else:
                messagebox.showerror("Erro", "Arquivo não encontrado.")
        else:
            messagebox.showwarning("Aviso", "Selecione um exame para abrir.")

    tk.Button(pesquisa_frame, text="Pesquisar", command=pesquisar_exames).grid(row=2, column=0, padx=5, pady=10)
    tk.Button(pesquisa_frame, text="Abrir Exame", command=abrir_exame).grid(row=2, column=1, padx=5, pady=10)

    pesquisa_frame.grid_columnconfigure(1, weight=1)
    pesquisa_frame.grid_rowconfigure(1, weight=1)

def abrir_analise_de_pacientes():
    analise_janela = tk.Toplevel(root)
    analise_janela.title("Análise de Pacientes")
    analise_janela.geometry("700x400")
    analise_janela.config(background=BRANCO)

    # Frame para a lista de pacientes
    lista_frame = tk.Frame(analise_janela)
    lista_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    # Criação da Treeview para exibir os pacientes
    colunas = ('Nome', 'Idade', 'CPF', 'Próxima Consulta')
    tree = ttk.Treeview(lista_frame, columns=colunas, show='headings')

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    tree.pack(side='left', fill='both', expand=True)

    # Scrollbar para a Treeview
    scrollbar = ttk.Scrollbar(lista_frame, orient='vertical', command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)

    # Frame para pesquisa e botões
    controle_frame = tk.Frame(analise_janela)
    controle_frame.pack(pady=10)

    # Campo de pesquisa
    tk.Label(controle_frame, text="Pesquisar paciente:").grid(row=0, column=0, padx=5)
    pesquisa_entry = tk.Entry(controle_frame)
    pesquisa_entry.grid(row=0, column=1, padx=5)

    def carregar_pacientes():
        tree.delete(*tree.get_children())
        with open('pacientes.csv', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                proxima_consulta = obter_proxima_consulta(row[0])
                tree.insert('', 'end', values=row + [proxima_consulta])

    def obter_proxima_consulta(nome_paciente):
        hoje = datetime.now().date()
        proxima_consulta = "Sem agendamento"
        with open('consultas.csv', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == nome_paciente:
                    data_consulta = datetime.strptime(row[2], "%m/%d/%y").date()
                    if data_consulta >= hoje:
                        proxima_consulta = row[2]
                        break
        return proxima_consulta

    def pesquisar_paciente():
        termo_pesquisa = pesquisa_entry.get().lower()
        tree.delete(*tree.get_children())
        with open('pacientes.csv', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if termo_pesquisa in row[0].lower():
                    proxima_consulta = obter_proxima_consulta(row[0])
                    tree.insert('', 'end', values=row + [proxima_consulta])

    def mostrar_agendamentos_semana():
        agendamentos_janela = tk.Toplevel(analise_janela)
        agendamentos_janela.title("Agendamentos da Semana")
        agendamentos_janela.geometry("500x300")

        agendamentos_tree = ttk.Treeview(agendamentos_janela, columns=('Data', 'Paciente', 'Tipo'), show='headings')
        for col in ('Data', 'Paciente', 'Tipo'):
            agendamentos_tree.heading(col, text=col)
            agendamentos_tree.column(col, width=100)

        agendamentos_tree.pack(fill='both', expand=True)

        hoje = datetime.now().date()
        fim_semana = hoje + timedelta(days=7)

        with open('consultas.csv', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                data_consulta = datetime.strptime(row[2], "%m/%d/%y").date()
                if hoje <= data_consulta < fim_semana:
                    agendamentos_tree.insert('', 'end', values=(row[2], row[0], row[1]))

    def excluir_paciente():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Por favor, selecione um paciente para excluir.")
            return

        paciente_data = tree.item(selected_item)['values']
        resposta = messagebox.askyesno("Confirmar Exclusão", f"Tem a certeza de que deseja excluir o paciente {paciente_data[0]}?")

        if resposta:
            # Remover o paciente do CSV de pacientes
            linhas_atualizadas = []
            with open('pacientes.csv', 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] != paciente_data[0]:
                        linhas_atualizadas.append(row)

            with open('pacientes.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(linhas_atualizadas)

            # Remover as consultas do paciente do CSV de consultas
            consultas_atualizadas = []
            with open('consultas.csv', 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] != paciente_data[0]:
                        consultas_atualizadas.append(row)

            with open('consultas.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(consultas_atualizadas)

            tree.delete(selected_item)
            messagebox.showinfo("Sucesso", "Paciente excluído com sucesso!")

    def editar_paciente():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Por favor, selecione um paciente para editar.")
            return

        paciente_data = tree.item(selected_item)['values']
        editar_janela = tk.Toplevel(analise_janela)
        editar_janela.title(f"Editar Paciente: {paciente_data[0]}")
        editar_janela.geometry("400x300")

        tk.Label(editar_janela, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        nome_entry = tk.Entry(editar_janela)
        nome_entry.insert(0, paciente_data[0])
        nome_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(editar_janela, text="Idade:").grid(row=1, column=0, padx=5, pady=5)
        idade_entry = tk.Entry(editar_janela)
        idade_entry.insert(0, paciente_data[1])
        idade_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(editar_janela, text="CPF:").grid(row=2, column=0, padx=5, pady=5)
        cpf_entry = tk.Entry(editar_janela)
        cpf_entry.insert(0, paciente_data[2])
        cpf_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(editar_janela, text="Próxima Consulta:").grid(row=3, column=0, padx=5, pady=5)
        consulta_entry = tk.Entry(editar_janela)
        consulta_entry.insert(0, paciente_data[3])
        consulta_entry.grid(row=3, column=1, padx=5, pady=5)

        def salvar_alteracoes():
            novo_nome = nome_entry.get()
            nova_idade = idade_entry.get()
            novo_cpf = cpf_entry.get()
            nova_consulta = consulta_entry.get()

            # Atualizar o CSV de pacientes
            linhas_atualizadas = []
            with open('pacientes.csv', 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == paciente_data[0]:
                        row = [novo_nome, nova_idade, novo_cpf]
                    linhas_atualizadas.append(row)

            with open('pacientes.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(linhas_atualizadas)

            # Atualizar o CSV de consultas
            linhas_atualizadas = []
            with open('consultas.csv', 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == paciente_data[0] and row[2] == paciente_data[3]:
                        row = [novo_nome, row[1], nova_consulta]
                    linhas_atualizadas.append(row)

            with open('consultas.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(linhas_atualizadas)

            # Atualizar a Treeview
            tree.item(selected_item, values=(novo_nome, nova_idade, novo_cpf, nova_consulta))

            messagebox.showinfo("Sucesso", "Dados do paciente atualizados com sucesso!")
            editar_janela.destroy()

        tk.Button(editar_janela, text="Salvar Alterações", command=salvar_alteracoes).grid(row=4, column=0, columnspan=2, pady=10)

    # Botões
    tk.Button(controle_frame, text="Pesquisar", command=pesquisar_paciente).grid(row=0, column=2, padx=5)
    tk.Button(controle_frame, text="Mostrar Todos", command=carregar_pacientes).grid(row=0, column=3, padx=5)
    tk.Button(controle_frame, text="Agendamentos da Semana", command=mostrar_agendamentos_semana).grid(row=0, column=4, padx=5)
    tk.Button(controle_frame, text="Editar Paciente", command=editar_paciente).grid(row=0, column=5, padx=5)
    tk.Button(controle_frame, text="Excluir Paciente", command=excluir_paciente).grid(row=0, column=5, padx=5)
    carregar_pacientes()  # Carrega todos os pacientes inicialmente



# Janela de Login
login_janela = tk.Tk()
login_janela.title("Login")
login_janela.geometry("300x200")
login_janela.configure(bg=BRANCO)

frame_login = tk.Frame(login_janela, bg=BRANCO)
frame_login.pack(expand=True, padx=20, pady=20)

tk.Label(frame_login, text="Clínica Odontológica", font=FONTE_TITULO, bg=BRANCO, fg=AZUL_CLARO).grid(row=0, column=0, columnspan=2, pady=(0, 20))

tk.Label(frame_login, text="Usuário", font=FONTE_CORPO, bg=BRANCO, fg=CINZA_ESCURO).grid(row=1, column=0, sticky="e", padx=5, pady=5)
usuario_entry = tk.Entry(frame_login, font=FONTE_CORPO, bg=CINZA_CLARO, relief=tk.FLAT, bd=1)
usuario_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_login, text="Senha", font=FONTE_CORPO, bg=BRANCO, fg=CINZA_ESCURO).grid(row=2, column=0, sticky="e", padx=5, pady=5)
senha_entry = tk.Entry(frame_login, show="*", font=FONTE_CORPO, bg=CINZA_CLARO, relief=tk.FLAT, bd=1)
senha_entry.grid(row=2, column=1, padx=5, pady=5)

login_btn = tk.Button(frame_login, text="Login", command=verificar_login, bg=AZUL_CLARO, fg=BRANCO, font=FONTE_DESTAQUE, relief=tk.FLAT, bd=0, padx=20, pady=5)
login_btn.grid(row=3, columnspan=2, pady=(20, 0))
login_btn.bind("<Enter>", lambda e: e.widget.configure(bg=VERDE_MENTA))
login_btn.bind("<Leave>", lambda e: e.widget.configure(bg=AZUL_CLARO))

aplicar_estilo(login_janela)

login_janela.mainloop()