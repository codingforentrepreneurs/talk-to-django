from typing import List
from django.apps import apps
from sqlalchemy import make_url, create_engine
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.retrievers import NLSQLRetriever

from . import db, settings, prompts

EMEDDING_LENGTH = settings.EMEDDING_LENGTH

settings.init()

def get_vector_store(
        vector_db_name=settings.VECTOR_DB_NAME, vector_db_table_name=settings.VECTOR_DB_TABLE_NAME
    ):
    db_url = db.get_database_url(use_pooling=True)
    url = make_url(db_url)
    return PGVectorStore.from_params(
        database=vector_db_name,
        host=url.host,
        password=url.password,
        port=url.port or 5432,
        user=url.username,
        table_name=vector_db_table_name,
        embed_dim=EMEDDING_LENGTH,
    )

def get_semantic_query_index():
    vector_store = get_vector_store()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)

def get_semantic_query_retriever_engine(top_k=5):
    index = get_semantic_query_index()
    retriever = index.as_retriever(similarity_top_k=top_k)
    retriever.retrieve_mode = 'embedding'
    return RetrieverQueryEngine.from_args(
        retriever
    )

def get_semantic_query_engine():
    index = get_semantic_query_index()
    return index.as_query_engine()


def get_default_sql_engine_tables() -> List[str]:
    BlogPost = apps.get_model("blog", "BlogPost")
    PageView = apps.get_model("analytics", "PageView")
    tables = []
    models = [BlogPost, PageView]
    for model in models:
        table = model._meta.db_table
        tables.append(table)
    return tables


def get_llamaindex_sql_database() -> SQLDatabase:
    """
    Using django database 
    Not using the LlamaIndex Vector db like
    `get_vector_store`
    """
    tables = get_default_sql_engine_tables()
    database_url = db.get_database_url(use_pooling=True)
    engine = create_engine(database_url)
    return SQLDatabase(engine, include_tables=tables)

def get_sql_query_engine(*args, **kwargs) -> NLSQLTableQueryEngine:
    tables = get_default_sql_engine_tables()
    sql_database = get_llamaindex_sql_database()
    config = {
        "sql_database": sql_database,
        "tables": tables,
        "response_synthesis_prompt": prompts.custom_sql_response_synthesis_prompt,
        "text_to_sql_prompt": prompts.custom_text_to_sql_prompt
    }
    config.update(**kwargs)
    return NLSQLTableQueryEngine(*args, **config)

def get_sql_query_retriever(*args, **kwargs) -> NLSQLRetriever:
    tables = get_default_sql_engine_tables()
    sql_database = get_llamaindex_sql_database()
    config = {
        "sql_database": sql_database,
        "tables": tables,
        "response_synthesis_prompt": prompts.custom_sql_response_synthesis_prompt,
        "text_to_sql_prompt": prompts.custom_text_to_sql_prompt
    }
    config.update(**kwargs)
    return NLSQLRetriever(*args, **config)