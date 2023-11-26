from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from drf_spectacular.utils import extend_schema
from django.urls import reverse

from simpleblog.api.pagination import  LimitOffsetPagination, get_paginated_response_context
from simpleblog.post.models import  Article
from simpleblog.post.selectors import article_list, article_detail
from simpleblog.post.services import post_create


class ArticleApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class OutPutPostSerializer(serializers.ModelSerializer):
        author = serializers.SerializerMethodField("get_author")
        url = serializers.SerializerMethodField("get_url")

        class Meta:
            model = Article
            fields = ("id", "title", "slug", "author", "created_at", "updated_at", "url")

        def get_author(self, post):
            return post.author.username

        def get_url(self, post):
            request = self.context.get("request")
            path = reverse("api:post:post_detail", args=(post.id, post.slug,))
            return request.build_absolute_uri(path)

    @extend_schema(
        responses=OutPutPostSerializer,
    )
    def get(self, request):

        try:
            query = article_list().select_related('author')
        except Exception as ex:
            return Response(
                {"detail": "Filter Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.OutPutPostSerializer,
            queryset=query,
            request=request,
            view=self,
        )


class PostDetailApi(APIView):

    class OutPutPostDetailSerializer(serializers.ModelSerializer):
        author = serializers.SerializerMethodField("get_author")

        class Meta:
            model = Article
            fields = ("id", "author", "slug", "title", "content", "created_at", "updated_at")

        def get_author(self, post):
            return post.author.username

    @extend_schema(
        responses=OutPutPostDetailSerializer,
    )
    def get(self, request, id, slug):

        try:
            query = article_detail(id=id, slug=slug)
        except Exception as ex:
            return Response(
                {"detail": "Filter Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.OutPutPostDetailSerializer(query)

        return Response(serializer.data)


