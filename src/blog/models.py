from django.db import models
from pgvector.django import VectorField
# Create your models here.

from . import services
EMEDDING_LENGTH=services.EMEDDING_LENGTH

class BlogPost(models.Model):
    # id -> models.AutoField()
    title = models.CharField(max_length=200)
    content = models.TextField()
    _content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    embedding = VectorField(dimensions=EMEDDING_LENGTH, blank=True, null=True)
    can_delete = models.BooleanField(default=False, help_text="Use in jupyter notebooks")

    def save(self, *args, **kwargs):
        has_changed = False
        if self._content != self.content:
            has_changed = True
            self._content = self.content
        if (self.embedding is None) or has_changed == True:
            raw_embedding_text = self.get_embedding_text_raw()
            if raw_embedding_text is not None:
                self.embedding = services.get_embedding(raw_embedding_text)
        super().save(*args, **kwargs) 

    def get_embedding_text_raw(self):
        return self.content