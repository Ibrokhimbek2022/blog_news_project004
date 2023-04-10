from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.


class Category(models.Model):
    title = models.CharField(verbose_name="Название категории", max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category_articles", kwargs={"category_id": self.pk})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Article(models.Model):
    title = models.CharField(verbose_name="Название статьи", max_length=100)
    content = models.TextField(verbose_name="Описание статьи")
    image = models.ImageField(verbose_name="Фотка стати", upload_to="photos/", blank=True, null=True)
    views = models.IntegerField(verbose_name="Кол-во просмотров", default=0)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now_add=True)
    category = models.ForeignKey(to=Category, verbose_name="Категория", on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, verbose_name="Автор", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"article_id": self.pk})

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()


class ArticleCountViews(models.Model):
    session_id = models.CharField(max_length=150, db_index=True, null=True, blank=True)
    article = models.ForeignKey(Article, null=True, blank=True, default=None, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
