# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

def get_engine():
    return create_engine('sqlite:///clinica.db', echo=False)

def create_tables(engine):
    Base.metadata.create_all(engine)

def get_session():
    engine = get_engine()
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    return Session()
