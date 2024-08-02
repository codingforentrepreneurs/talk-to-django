from decouple import config
from llama_index.llms.openai import OpenAI

from llama_index.core import Settings

from .embeddings import MyOpenAIEmbedding



LLM_MODEL = config("LLM_MODEL", default="gpt-4o")
EMEDDING_LENGTH = config("EMEDDING_LENGTH", default=1536, cast=int)
EMEDDING_MODEL =config("EMEDDING_MODEL", default="text-embedding-3-small")
OPENAI_API_KEY = config("OPENAI_API_KEY")

VECTOR_DB_NAME = config("VECTOR_DB_NAME", default='vector_db')
VECTOR_DB_TABLE_NAME = config("VECTOR_DB_TABLE_NAME", default='blogpost')

def init():
    llm = OpenAI(model=LLM_MODEL, api_key=OPENAI_API_KEY)
    embed_model = MyOpenAIEmbedding(model=EMEDDING_MODEL, api_key=OPENAI_API_KEY)
    Settings.llm = llm
    Settings.embed_model = embed_model
