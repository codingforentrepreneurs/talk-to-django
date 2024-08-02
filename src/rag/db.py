from decouple import config

from sqlalchemy import create_engine, text

from . import settings


def get_database_url(use_pooling=True):
    db_url_env = config("DATABASE_URL")
    if use_pooling:
        db_url_env = config("DATABASE_URL_POOL")
    if db_url_env.startswith("postgres://"):
        return db_url_env.replace("postgres://", "postgresql://", 1)
    return db_url_env


def init_vector_db():
    db_url = get_database_url(use_pooling=True)
    vector_db_name = settings.VECTOR_DB_NAME
    vector_db_name = settings.VECTOR_DB_TABLE_NAME
    engine = create_engine(db_url, isolation_level="AUTOCOMMIT")
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1 FROM pg_database WHERE datname = :db_name"), {"db_name": vector_db_name})
        db_exists = result.scalar() == 1
        if not db_exists:
            connection.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
            connection.execute(text(f"CREATE DATABASE {vector_db_name}"))