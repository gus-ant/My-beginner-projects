# app.py (continuação)

# app.py

import tkinter as tk
from tkinter import ttk, messagebox
from utils.excel_handler import initialize_excel_files, read_excel, append_to_excel, update_excel
import pandas as pd
from datetime import datetime

# Inicializar os arquivos Excel
initialize_excel_files()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clínica Odontológica")
        self.geometry("800x600")
        
        # Criar um menu
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # Menu de Pacientes
        paciente_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Pacientes", menu=paciente_menu)
        paciente_menu.add_command(label="Adicionar Paciente", command=self.adicionar_paciente)
        paciente_menu.add_command(label="Listar Pacientes", command=self.listar_pacientes)
        
        # Menu de Agendamentos
        agendamento_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Agendamentos", menu=agendamento_menu)
        agendamento_menu.add_command(label="Adicionar Agendamento", command=self.adicionar_agendamento)
        agendamento_menu.add_command(label="Listar Agendamentos", command=self.listar_agendamentos)
        
        # Outros menus podem ser adicionados aqui (Tratamentos, Receitas, Materiais)
    
    # Funções para Pacientes
    def adicionar_paciente(self):
        PacienteForm(self)
    
    def listar_pacientes(self):
        PacienteList(self)
    
    # Funções para Agendamentos
    def adicionar_agendamento(self):
        AgendamentoForm(self)
    
    def listar_agendamentos(self):
        AgendamentoList(self)

# Executar a aplicação
if __name__ == "__main__":
    app = App()
    app.mainloop()
