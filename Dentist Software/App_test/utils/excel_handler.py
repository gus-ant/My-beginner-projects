# utils/excel_handler.py

import pandas as pd
import os

DATA_DIR = 'data'

def initialize_excel_files():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    files = {
        'pacientes.xlsx': ['ID', 'Nome', 'Contato', 'Histórico Médico', 'Exames', 'Condições de Saúde'],
        'agendamentos.xlsx': ['ID', 'Paciente', 'Dentista', 'Data', 'Hora', 'Status'],
        'tratamentos.xlsx': ['ID', 'Paciente', 'Descrição', 'Data', 'Status'],
        'receitas.xlsx': ['ID', 'Paciente', 'Medicamento', 'Dosagem', 'Data'],
        'materiais.xlsx': ['ID', 'Nome', 'Quantidade', 'Descrição', 'Solicitação']
    }
    
    for file, columns in files.items():
        path = os.path.join(DATA_DIR, file)
        if not os.path.exists(path):
            df = pd.DataFrame(columns=columns)
            df.to_excel(path, index=False)
            print(f"Arquivo {file} criado.")

def read_excel(file_name):
    path = os.path.join(DATA_DIR, file_name)
    if os.path.exists(path):
        return pd.read_excel(path)
    else:
        print(f"Arquivo {file_name} não encontrado.")
        return pd.DataFrame()

def write_excel(file_name, df):
    path = os.path.join(DATA_DIR, file_name)
    df.to_excel(path, index=False)
    print(f"Dados gravados em {file_name} com sucesso.")

def append_to_excel(file_name, data):
    df = read_excel(file_name)
    df = df.append(data, ignore_index=True)
    write_excel(file_name, df)

def update_excel(file_name, df):
    write_excel(file_name, df)
