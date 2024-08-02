from django.apps import apps
from llama_index.core import Document

from . import engines

def update_llama_index_documents(use_saved_embeddings=True):
    vector_index = engines.get_semantic_query_index()
    BlogPost = apps.get_model("blog", "BlogPost")
    docs = []
    qs = BlogPost.objects.filter(can_delete=True)
    for obj in qs:
        doc_config = {
            "text": f"{obj.get_embedding_text_raw()}",
            "doc_id": str(obj.id),
            "metadata": {
                "pk": obj.pk,
                "title": obj.title
            }
        }
        if use_saved_embeddings:
            if obj.embedding is not None:
                doc_config['embedding'] = list(obj.embedding)
        docs.append(
            Document(**doc_config)
        )
    for doc in docs:
        vector_index.delete_ref_doc(f"{doc.id_}", delete_from_docstore=True)
        vector_index.insert(doc)