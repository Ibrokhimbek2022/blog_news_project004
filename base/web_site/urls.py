from django.urls import path
from . import views

urlpatterns = [
    # path("", views.home_page, name="home"),
    path("", views.HomePageView.as_view(), name="home"),
    path("search/", views.SearchResults.as_view(), name="search"),
    path("categories/<int:category_id>/", views.category_articles, name="category_articles"),
    path("articles/<int:article_id>/", views.article_detail, name="article_detail"),

    path("login/", views.login_view, name="login"),
    path("registration/", views.registration_view, name="registration"),
    path("logout/", views.user_logout, name="logout"),

    path("create_article/", views.create_article, name="create_article"),
    path("articles/<str:username>/", views.author_articles_view, name="author_articles"),
    path("update_article/<int:pk>/", views.UpdatePost.as_view(), name="update"),
    path("delete_article/<int:pk>/", views.DeletePost.as_view(), name="delete"),
    path("users/<int:pk>/profile/edit/", views.ChangeUserData.as_view(), name="profile"),

    path("comments/delete/<int:comment_id>/", views.delete_comment, name="delete_comment"),
    path("comments/edit/<int:pk>/", views.UpdateComment.as_view(), name="update_comment")
]

# http://127.0.0.1:8000/categories/2  запускается функция home_page
