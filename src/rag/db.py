from decouple import config

def get_database_url(use_pooling=True):
    db_url_env = config("DATABASE_URL")
    if use_pooling:
        db_url_env = config("DATABASE_URL_POOL")
    if db_url_env.startswith("postgres://"):
        return db_url_env.replace("postgres://", "postgresql://", 1)
    return db_url_env