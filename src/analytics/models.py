from django.db import models
from blog.models import BlogPost
# Create your models here.

class PageView(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)