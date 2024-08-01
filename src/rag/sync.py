
from blog.models import BlogPost
from llama_index.core import Document

from .engines import get_semantic_query_index

def get_blog_post_docs():
    docs = []
    qs = BlogPost.objects.filter(can_delete=True)
    for obj in qs:
        if obj.embedding is None:
            continue
        docs.append(
            Document(
                text=f"{obj.get_embedding_text_raw()}",
                doc_id=str(obj.id),
                embedding=obj.embedding.tolist(),
                metadata = {
                    "pk": obj.pk,
                    "title": obj.title
                }
            )
        )
    return docs


def sync_blog_docs():
    index = get_semantic_query_index()
    docs = get_blog_post_docs()
    print(f"Syncing {len(docs)} docs")
    for doc in docs:
        index.delete_ref_doc(f"{doc.id_}", delete_from_docstore=True)
        index.insert(doc)
    print("Sync done.")

