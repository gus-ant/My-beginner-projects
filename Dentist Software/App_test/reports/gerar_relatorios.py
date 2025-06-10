# reports/gerar_relatorios.py

import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from database import get_session
from models import Paciente, Dentista, Consulta, PlanoTratamento, Receita, Material
# reports/gerar_relatorios.py

import pandas as pd

def gerar_relatorio_pacientes(session):
    try:
        pacientes = session.query(Paciente).all()
        dados = []
        for p in pacientes:
            dados.append({
                "ID": p.id,
                "Nome": p.nome,
                "Contato": p.contato,
                "Histórico Médico": p.historico_medico,
                "Condições de Saúde": p.condicoes_saude
            })
        df = pd.DataFrame(dados)
        return df
    except Exception as e:
        print(f"Erro ao gerar relatório de pacientes: {e}")
        return None

def gerar_relatorio_consultas(session):
    try:
        consultas = session.query(Consulta).all()
        dados = []
        for c in consultas:
            dados.append({
                "ID": c.id,
                "Paciente": c.paciente.nome,
                "Dentista": c.dentista.nome,
                "Data": c.data.strftime("%d/%m/%Y"),
                "Hora": c.hora.strftime("%H:%M"),
                "Status": c.status
            })
        df = pd.DataFrame(dados)
        return df
    except Exception as e:
        print(f"Erro ao gerar relatório de consultas: {e}")
        return None

def gerar_relatorio_planos_tratamento(session):
    try:
        planos = session.query(PlanoTratamento).all()
        dados = []
        for p in planos:
            dados.append({
                "ID": p.id,
                "Paciente": p.paciente.nome,
                "Descrição": p.descricao
            })
        df = pd.DataFrame(dados)
        return df
    except Exception as e:
        print(f"Erro ao gerar relatório de planos de tratamento: {e}")
        return None

def gerar_relatorio_receitas(session):
    try:
        receitas = session.query(Receita).all()
        dados = []
        for r in receitas:
            dados.append({
                "ID": r.id,
                "Paciente": r.paciente.nome,
                "Medicamento": r.medicamento,
                "Dosagem": r.dosagem
            })
        df = pd.DataFrame(dados)
        return df
    except Exception as e:
        print(f"Erro ao gerar relatório de receitas: {e}")
        return None

def gerar_relatorio_materiais(session):
    try:
        materiais = session.query(Material).all()
        dados = []
        for m in materiais:
            dados.append({
                "ID": m.id,
                "Nome": m.nome,
                "Quantidade": m.quantidade,
                "Descrição": m.descricao
            })
        df = pd.DataFrame(dados)
        return df
    except Exception as e:
        print(f"Erro ao gerar relatório de materiais: {e}")
        return None
