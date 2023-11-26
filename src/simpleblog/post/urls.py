from django.urls import path

from simpleblog.post.apis.selectors import ArticleApi, PostDetailApi
from simpleblog.post.apis.services import CreateArticleApi

urlpatterns = [
    path("createarticle/", CreateArticleApi.as_view(), name="createarticle"),
    path("articles/", ArticleApi.as_view(), name="articles"),
    path("post_detail/<int:id>/<slug:slug>/", PostDetailApi.as_view(), name="post_detail"),
]