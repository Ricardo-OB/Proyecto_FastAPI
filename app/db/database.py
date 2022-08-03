from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings

SQLALCHEMY_DATABASE_URL = settings.database_url
engine = create_engine(url=SQLALCHEMY_DATABASE_URL)
session_local = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    except Exception:
        print('Error en la base de datos')
    finally:
        db.close()