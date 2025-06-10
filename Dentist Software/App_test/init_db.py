# init_db.py

from database import get_session

def init_db():
    session = get_session()
    print("Banco de dados inicializado e tabelas criadas.")

if __name__ == "__main__":
    init_db()
