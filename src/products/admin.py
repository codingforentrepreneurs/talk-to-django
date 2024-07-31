from django.contrib import admin

# Register your models here.
from .models import Product, Embedding


admin.site.register(Product)

admin.site.register(Embedding)