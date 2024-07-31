from openai import OpenAI
from decouple import config
from django.apps import apps
from pgvector.django import CosineDistance
from django.db.models import F

# https://platform.openai.com/docs/guides/embeddings/how-to-get-embeddings
EMEDDING_LENGTH=config("EMEDDING_LENGTH", default=1536, cast=int)
EMEDDING_MODEL =config("EMEDDING_MODEL", default="text-embedding-3-small")
OPENAI_API_KEY= config("OPENAI_API_KEY")

client = OpenAI(
    api_key=OPENAI_API_KEY
)

def get_embedding(text, model=EMEDDING_MODEL):
    text = text.replace("\n", " ").strip()
    return client.embeddings.create(input=[text], model=model).data[0].embedding

def get_query_embedding(text):
    # get_or_create Query Embedding model
    return get_embedding(text)

def search_posts(query, limit=5):
    BlogPost = apps.get_model(app_label='blog', model_name='BlogPost')
    query_embedding = get_query_embedding(query)
    qs = BlogPost.objects.annotate(
        distance=CosineDistance('embedding',query_embedding),
        similarity=1 - F("distance")
    ).order_by("distance")[:limit]
    return qs