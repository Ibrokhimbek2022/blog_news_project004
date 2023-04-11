from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.views import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DeleteView, ListView

from .forms import LoginForm, RegistrationForm, ArticleForm, CommentForm, CustomUserChangeForm
from .models import Category, Article, Comment, ArticleCountViews
from django.utils.datetime_safe import datetime


# Create your views here.


# Отображение главной страницы с помощью класса
class HomePageView(ListView):
    model = Article
    template_name = "pages/index.html"
    context_object_name = "articles"


class SearchResults(HomePageView):
    def get_queryset(self):
        query = self.request.GET.get("q")
        return Article.objects.filter(
            Q(title__iregex=query) | Q(content__iregex=query)
        )


# def home_page(request):
#     categories = Category.objects.all()
#     articles = Article.objects.all()
#     context = {
#         "categories": categories,
#         "articles": articles
#     }
#     return render(request, "pages/index.html", context)


def category_articles(request, category_id):
    category = Category.objects.filter(pk=category_id).first()
    articles = Article.objects.filter(category=category)

    context = {
        "articles": articles
    }
    return render(request, "pages/index.html", context)


def article_detail(request, article_id):
    article = Article.objects.filter(pk=article_id).first()

    if not request.session.session_key:
        request.session.save()

    session_id = request.session.session_key
    if not request.user.is_authenticated:
        views_items = ArticleCountViews.objects.filter(session_id=session_id, article=article)
        if not views_items.count() and str(session_id) != "None":
            views = ArticleCountViews()
            views.article = article
            views.session_id = session_id
            views.save()

            article.views += 1
            article.save()
    else:
        views_items = ArticleCountViews.objects.filter(article=article,
                                                       user=request.user)
        if not views_items.count():
            views = ArticleCountViews()
            views.article = article
            views.user = request.user
            views.save()

            article.views += 1
            article.save()

    if request.method == "POST":
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.article = article
            form.author = request.user
            form.save()
            return redirect("article_detail", article.pk)
    else:
        form = CommentForm()

    comments = Comment.objects.filter(article=article)

    context = {
        "article": article,
        "title": article.title,
        "form": form,
        "comments": comments
    }
    return render(request, "pages/article_detail.html", context)


def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = LoginForm()

    context = {
        "form": form
    }

    return render(request, "pages/login.html", context)


def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegistrationForm()

    context = {
        "form": form
    }

    return render(request, "pages/registration.html", context)


# http://127.0.0.0:8000/user22/articles/


def user_logout(request):
    logout(request)
    return redirect("home")


@login_required(login_url="login")
def create_article(request):
    if request.method == "POST":
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect("article_detail", form.pk)
    else:
        form = ArticleForm()

    context = {
        "form": form
    }
    return render(request, "pages/article_form.html", context)


@login_required(login_url="login")
def author_articles_view(request, username):
    author = User.objects.get(username=username)
    articles = Article.objects.filter(author=author)

    total_views = sum([article.views for article in articles])
    total_comments = sum([article.comment_set.all().count() for article in articles])
    days_left = datetime.now().date() - author.date_joined.date()

    context = {
        "articles": articles,
        "total_views": total_views,
        "total_comments": total_comments,
        "total_posts": articles.count(),
        "days_left": days_left.days
    }
    return render(request, "pages/my_articles.html", context)


class UpdatePost(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "pages/article_form.html"


class DeletePost(DeleteView):
    model = Article
    success_url = "/"
    template_name = "pages/article_confirm_delete.html"


class ChangeUserData(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = "pages/profile.html"
    success_url = "home"


def delete_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    article_id = comment.article.pk
    comment.delete()

    return redirect("article_detail", article_id)


class UpdateComment(UpdateView):
    model = Comment
    template_name = "pages/article_detail.html"
    form_class = CommentForm

    def form_valid(self, form):
        obj = self.get_object()
        article = Article.objects.get(pk=obj.article.pk)
        form.save()
        return redirect("article_detail", article.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        article = Article.objects.get(pk=obj.article.pk)
        comments = Comment.objects.filter(article=article)
        context["article"] = article
        context["comments"] = comments

        return context

# TODO: DONE
# TODO 2) СДЕЛАТЬ ПОИСК  +
# TODO 5) СДЕЛАТЬ ИЗМЕНЕНИЕ АДМИНКИ +
# TODO 2) СДЕЛАТЬ УДАЛЕНИЕ КОММЕНТАРИЯ +
# TODO 3) СДЕЛАТЬ ИЗМЕНЕНИЯ КОММЕНТАРИЯ +
# TODO 1) СДЕЛАТЬ КОЛИЧЕСТВО ПРОСМОТРОВ +
# TODO 3) СДЕЛАТЬ СТРАНИЦУ ПРОФИЛЯ

# ОСТАЛОСЬ СДЕЛАТЬ:
# TODO 4) СДЕЛАТЬ ИЗМЕНЕНИЕ ПРОФИЛЯ


# Предложения:
# TODO 1) СДЕЛАТЬ ОТВЕТ НА КОММЕНТАРИЙ
# TODO 4) СДЕЛАТЬ РАЗВОРАЧИВАНИЕ КОММЕНТАРИЯ ЕСЛИ СЛИШКОМ ДЛИННЫЙ
# TODO 5) СДЕЛАТЬ ЛАЙК ДИЗЛАЙК
