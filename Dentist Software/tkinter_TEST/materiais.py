import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
from datetime import datetime
from tkcalendar import Calendar

# Função para verificar login
def verificar_login():
    usuario = usuario_entry.get()
    senha = senha_entry.get()
    
    if usuario == "user" and senha == "1234":
        messagebox.showinfo("Sucesso", "Login bem-sucedido!")
        abrir_pagina_principal()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos!")

# Função para abrir a página principal
def abrir_pagina_principal():
    login_janela.destroy()  # Fecha a janela de login
    global root
    root = tk.Tk()
    root.title("Clínica Odontológica")
    
    # Título
    titulo = tk.Label(root, text="Clínica Odontológica - Sistema de Gerenciamento", font=("Helvetica", 16, "bold"))
    titulo.pack(pady=10)

    # Botão para Cadastro de Pacientes
    cadastro_btn = tk.Button(root, text="Cadastro de Paciente", command=abrir_pagina_cadastro, width=30)
    cadastro_btn.pack(pady=5)

    # Botão para abrir a lista de materiais
    materiais_btn = tk.Button(root, text="Lista de Materiais", command=abrir_lista_materiais, width=30)
    materiais_btn.pack(pady=5)

    # Botão para upload de exames
    upload_btn = tk.Button(root, text="Upload de Exames", command=abrir_upload_exames, width=30)
    upload_btn.pack(pady=5)

    # Botão para agendar consulta
    agendar_btn = tk.Button(root, text="Agendar Consulta", command=abrir_agendar_consulta, width=30)
    agendar_btn.pack(pady=5)

# Função para abrir a página de agendar consultas
def abrir_agendar_consulta():
    agendar_janela = tk.Toplevel(root)
    agendar_janela.title("Agendar Consulta")

    tk.Label(agendar_janela, text="Selecione a data da consulta:").pack(pady=10)

    # Criação do calendário
    calendario = Calendar(agendar_janela, selectmode='day')
    calendario.pack(pady=10)

    def agendar():
        data_selecionada = calendario.get_date()
        # Aqui, você pode adicionar lógica para salvar a consulta em um arquivo CSV ou em um banco de dados
        messagebox.showinfo("Sucesso", f"Consulta agendada para {data_selecionada}")

    tk.Button(agendar_janela, text="Agendar Consulta", command=agendar).pack(pady=10)

# Função para abrir a página de cadastro de paciente
def abrir_pagina_cadastro():
    cadastro_janela = tk.Toplevel(root)
    cadastro_janela.title("Cadastro de Paciente")
    
    tk.Label(cadastro_janela, text="Nome do Paciente").grid(row=0, column=0)
    nome_entry = tk.Entry(cadastro_janela)
    nome_entry.grid(row=0, column=1)

    tk.Label(cadastro_janela, text="Idade").grid(row=1, column=0)
    idade_entry = tk.Entry(cadastro_janela)
    idade_entry.grid(row=1, column=1)

    tk.Label(cadastro_janela, text="CPF").grid(row=2, column=0)
    cpf_entry = tk.Entry(cadastro_janela)
    cpf_entry.grid(row=2, column=1)

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

# Função para abrir a página da lista de materiais
def abrir_lista_materiais():
    materiais_janela = tk.Toplevel(root)
    materiais_janela.title("Lista de Materiais")

    try:
        with open('materiais.csv', newline='') as file:
            reader = csv.reader(file)
            materiais = list(reader)
    except FileNotFoundError:
        materiais = []

    tk.Label(materiais_janela, text="ID").grid(row=0, column=0)
    tk.Label(materiais_janela, text="Nome do Material").grid(row=0, column=1)
    tk.Label(materiais_janela, text="Quantidade").grid(row=0, column=2)

    for i, material in enumerate(materiais, start=1):
        tk.Label(materiais_janela, text=material[0]).grid(row=i, column=0)
        tk.Label(materiais_janela, text=material[1]).grid(row=i, column=1)
        tk.Label(materiais_janela, text=material[2]).grid(row=i, column=2)

# Função para abrir a página de upload de exames
def abrir_upload_exames():
    upload_janela = tk.Toplevel(root)
    upload_janela.title("Upload de Exames (PDF)")
    
    tk.Label(upload_janela, text="Nome do Paciente").grid(row=0, column=0)
    nome_entry = tk.Entry(upload_janela)
    nome_entry.grid(row=0, column=1)

    def verificar_paciente():
        nome = nome_entry.get()
        encontrado = False
        with open('pacientes.csv', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == nome:
                    encontrado = True
                    break
        if encontrado:
            messagebox.showinfo("Sucesso", "Paciente encontrado, pronto para upload!")
            # Código para upload de PDF seria adicionado aqui
        else:
            messagebox.showwarning("Erro", "Paciente não cadastrado.")

    tk.Button(upload_janela, text="Verificar e Fazer Upload", command=verificar_paciente).grid(row=1, columnspan=2)

# Janela de Login
login_janela = tk.Tk()
login_janela.title("Login")

tk.Label(login_janela, text="Usuário").grid(row=0, column=0)
usuario_entry = tk.Entry(login_janela)
usuario_entry.grid(row=0, column=1)

tk.Label(login_janela, text="Senha").grid(row=1, column=0)
senha_entry = tk.Entry(login_janela, show="*")
senha_entry.grid(row=1, column=1)

tk.Button(login_janela, text="Login", command=verificar_login).grid(row=2, columnspan=2)

login_janela.mainloop()
