from django.db import models

# Create your models here.
class BlogPost(models.Model):
    # id -> models.AutoField()
    title = models.CharField(max_length=200)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # embedding