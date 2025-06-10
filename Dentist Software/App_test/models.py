# models.py

from sqlalchemy import create_engine, Column, Integer, String, Date, Time, ForeignKey, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Dentista(Base):
    __tablename__ = 'dentistas'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    especialidade = Column(String)
    
    consultas = relationship('Consulta', back_populates='dentista')

class Paciente(Base):
    __tablename__ = 'pacientes'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    contato = Column(String)
    historico_medico = Column(Text)
    condicoes_saude = Column(Text)
    
    consultas = relationship('Consulta', back_populates='paciente')
    planos_tratamento = relationship('PlanoTratamento', back_populates='paciente')
    receitas = relationship('Receita', back_populates='paciente')

class Consulta(Base):
    __tablename__ = 'consultas'
    
    id = Column(Integer, primary_key=True)
    data = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    status = Column(String, default='Agendada')  # Agendada, Realizada, Cancelada
    paciente_id = Column(Integer, ForeignKey('pacientes.id'))
    dentista_id = Column(Integer, ForeignKey('dentistas.id'))
    
    paciente = relationship('Paciente', back_populates='consultas')
    dentista = relationship('Dentista', back_populates='consultas')

class PlanoTratamento(Base):
    __tablename__ = 'planos_tratamento'
    
    id = Column(Integer, primary_key=True)
    descricao = Column(Text, nullable=False)
    paciente_id = Column(Integer, ForeignKey('pacientes.id'))
    
    paciente = relationship('Paciente', back_populates='planos_tratamento')

class Receita(Base):
    __tablename__ = 'receitas'
    
    id = Column(Integer, primary_key=True)
    medicamento = Column(String, nullable=False)
    dosagem = Column(String)
    paciente_id = Column(Integer, ForeignKey('pacientes.id'))
    
    paciente = relationship('Paciente', back_populates='receitas')

class Material(Base):
    __tablename__ = 'materiais'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    quantidade = Column(Integer, default=0)
    descricao = Column(Text)
