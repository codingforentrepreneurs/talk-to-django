from django.contrib import admin

# Register your models here.
from .models import BlogPost

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    readonly_fields = ['timestamp']

admin.site.register(BlogPost, BlogPostAdmin)