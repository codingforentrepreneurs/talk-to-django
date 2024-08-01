

from sqlalchemy import make_url

from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.query_engine import RetrieverQueryEngine

from . import db, settings

EMEDDING_LENGTH = settings.EMEDDING_LENGTH

settings.init()

def get_vector_store(
        vector_db_name="vector_db", vector_db_table_name="blogpost"
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