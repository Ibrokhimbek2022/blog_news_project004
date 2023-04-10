from django.contrib import admin
from .models import Category, Article, Comment

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "views", "created_at", "updated_at", "category", "author")
    list_display_links = ("pk", "title")
    list_editable = ("category", "author")
    list_filter = ("category",)


admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
