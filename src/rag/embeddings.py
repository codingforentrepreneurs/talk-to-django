from typing import List

from llama_index.embeddings.openai import OpenAIEmbedding

class MyOpenAIEmbedding(OpenAIEmbedding):
    def _get_query_embedding(self, query: str) -> List[float]:
        """Get query embedding."""
        # print('my query', query) 
        # obj, created = Query.objects.get_or_create(query=query)
        # obj.get_query_embedding()
        return super()._get_query_embedding(query)

    def _get_text_embedding(self, text: str) -> List[float]:
        """Get text embedding."""
        # print("texts", text)
        return super()._get_text_embedding(text)

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get text embeddings.

        By default, this is a wrapper around _get_text_embedding.
        Can be overridden for batch queries.
        """
        # print("texts", texts)
        return super()._get_text_embeddings(texts)