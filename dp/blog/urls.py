from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .apis.post import PostApi, PostDetailApi, PostDeleteApi, PostUpdateApi, PostAllApi
from .apis.subscription import SubscribeApi, UnsubscribeApi


app_name = "blog"
urlpatterns = [
        path("subscribe/",               SubscribeApi.as_view(), name="subscribe"),
        path("subscribe/<str:username>", UnsubscribeApi.as_view(), name="subscribe_detail"),
        path("post/",                    PostApi.as_view(), name="post"),
        path("postAll/",                 PostAllApi.as_view(), name="post"),
        path("post/post_detail/<int:id>/<slug:slug>/",PostDetailApi.as_view(), name="post_detail"),
        path("post/del/<int:id>",        PostDeleteApi.as_view(), name="post_delete"),
        path("post/edit/<int:id>",       PostUpdateApi.as_view(), name="post_update"),
        ]