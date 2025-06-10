# app.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from database import get_session
from models import Paciente, Dentista, Consulta, PlanoTratamento, Receita, Material
from reports.gerar_relatorios import gerar_relatorio_planos_tratamento, gerar_relatorio_pacientes, gerar_relatorio_consultas, gerar_relatorio_receitas, gerar_relatorio_materiais

def gerar_relatorio():
    tipo_relatorio = tipo_relatorio_var.get()
    
    if tipo_relatorio == "Pacientes":
        data = gerar_relatorio_pacientes(session)
    elif tipo_relatorio == "Consultas":
        data = gerar_relatorio_consultas(session)
    elif tipo_relatorio == "Planos de Tratamento":
        data = gerar_relatorio_planos_tratamento(session)
    elif tipo_relatorio == "Receitas":
        data = gerar_relatorio_receitas(session)
    elif tipo_relatorio == "Materiais":
        data = gerar_relatorio_materiais(session)
    else:
        messagebox.showerror("Erro", "Selecione um tipo de relatório válido.")
        return
    
    if data is not None and not data.empty:
        # Salvar o relatório em um arquivo Excel
        arquivo = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                              filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if arquivo:
            try:
                data.to_excel(arquivo, index=False)
                messagebox.showinfo("Sucesso", f"Relatório salvo em {arquivo}")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível salvar o relatório: {e}")
    else:
        messagebox.showwarning("Aviso", "Nenhum dado disponível para gerar o relatório.")

# Inicializar o banco de dados
session = get_session()

# Criar a janela principal
root = tk.Tk()
root.title("Clínica Odontológica - Gerar Relatórios")
root.geometry("400x250")
root.resizable(False, False)

# Variável para armazenar o tipo de relatório selecionado
tipo_relatorio_var = tk.StringVar()

# Label
label = ttk.Label(root, text="Selecione o tipo de relatório:", font=("Arial", 12))
label.pack(pady=10)

# Combobox para selecionar o tipo de relatório
combo = ttk.Combobox(root, textvariable=tipo_relatorio_var, state="readonly")
combo['values'] = ("Pacientes", "Consultas", "Planos de Tratamento", "Receitas", "Materiais")
combo.current(0)
combo.pack(pady=5)

# Botão para gerar relatório
btn_gerar = ttk.Button(root, text="Gerar Relatório", command=gerar_relatorio)
btn_gerar.pack(pady=20)

# Executar a aplicação
root.mainloop()
