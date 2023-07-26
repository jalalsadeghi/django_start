from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from drf_spectacular.utils import extend_schema
from django.urls import reverse

from dp.api.pagination import get_paginated_response, LimitOffsetPagination, get_paginated_response_context
from rest_framework.pagination import PageNumberPagination

from dp.blog.models import Post 
from dp.blog.selectors.posts import post_detail, post_list,postAll_list
from dp.blog.services.post import post_create, post_delete,post_update

from dp.files.services import FileStandardUploadService

from dp.api.mixins import ApiAuthMixin

from typing import Optional

class PostAllApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class OutPutPostAllSerializer(serializers.ModelSerializer):
        author = serializers.SerializerMethodField("get_author")
        url = serializers.SerializerMethodField("get_url")
        image_url = serializers.SerializerMethodField("get_image_url")

        class Meta:
            model = Post
            fields = ("id", "title", "url", "author", "image_url")

        def get_author(self, post) -> Optional[str]:
            return post.author.username
        
        def get_url(self, post) -> Optional[str]:
            request = self.context.get("request")
            path = reverse("api:blog:post_detail", args=(post.id, post.slug,))
            return request.build_absolute_uri(path)

        def get_image_url(self, post) -> Optional[str]:
            if post.image_id:
                return post.image.url
            
    @extend_schema(
        responses=OutPutPostAllSerializer,
    )
    def get(self, request):

        try:
            query = postAll_list()
        except Exception as ex:
            return Response(
                {"detail": "Filter Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.OutPutPostAllSerializer,
            queryset=query,
            request=request,
            view=self,
        )
        return data


class PostApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterPostSerializer(serializers.Serializer):
        title               = serializers.CharField(required=False, max_length=100)
        search              = serializers.CharField(required=False, max_length=100)
        created_at__range   = serializers.CharField(required=False, max_length=100)
        author__in          = serializers.CharField(required=False, max_length=100)
        slug                = serializers.CharField(required=False, max_length=100)
        content             = serializers.CharField(required=False, max_length=1000)
        id                  = serializers.IntegerField(required=False)

    class InputPostSerializer(serializers.Serializer):
        title   = serializers.CharField(max_length=100)
        content = serializers.CharField(max_length=1000)
        file    = serializers.FileField(required=False)

    class OutPutPostSerializer(serializers.ModelSerializer):
        author  = serializers.SerializerMethodField("get_author")
        url     = serializers.SerializerMethodField("get_url")
        image_url= serializers.SerializerMethodField("get_image_url")

        class Meta:
            model = Post
            fields = ("id", "url", "title", "content", "author", "image_url")

        def get_author(self, post) -> Optional[str]:
            return post.author.username

        def get_url(self, post) -> Optional[str]:
            request = self.context.get("request")
            path    = reverse("api:blog:post_detail", args=(post.id, post.slug,))
            return request.build_absolute_uri(path)

        def get_image_url(self, post) -> Optional[str]:
            if post.image_id:
                return post.image.url


    @extend_schema(
        responses   = OutPutPostSerializer,
        request     = InputPostSerializer,
    )
    def post(self, request):
        serializer = self.InputPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_id = 0
        file =  serializer.validated_data.get("file")
        if file:
            img_service = FileStandardUploadService(user=request.user, file_obj=serializer.validated_data.get("file"))
            file = img_service.create()
            file_id = file.id

        try: 
            query = post_create(
                user    = request.user,
                title   = serializer.validated_data.get("title"),
                content = serializer.validated_data.get("content"),
                image_id= file_id,
            )
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # return Response(status=status.HTTP_200_OK)
        # return Response(self.OutPutPostSerializer(query, context={"request":request}).data)
        return Response("file:",file)

    @extend_schema(
        parameters=[FilterPostSerializer],
        responses=OutPutPostSerializer,
    )
    def get(self, request):
        filters_serializer = self.FilterPostSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        # reset_queries()
        try:
            query = post_list(filters=filters_serializer.validated_data, user=request.user)
        except Exception as ex:
            return Response(
                {"detail": "Filter Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.OutPutPostSerializer,
            queryset=query,
            request=request,
            view=self,
        )
        return data


class PostDetailApi(ApiAuthMixin, APIView):

    class OutPutPostDetailSerializer(serializers.ModelSerializer):
        author = serializers.SerializerMethodField("get_author")

        class Meta:
            model = Post
            fields = ("id", "author", "slug", "title", "content", "created_at", "updated_at")

        def get_author(self, post) -> Optional[str]:
            return post.author.username


    @extend_schema(
        responses=OutPutPostDetailSerializer,
    )
    def get(self, request, id, slug):

        try:
            query = post_detail(id=id, slug=slug, user=request.user)
        except Exception as ex:
            return Response(
                {"detail": "Filter Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.OutPutPostDetailSerializer(query)

        return Response(serializer.data) 
    
class PostUpdateApi(ApiAuthMixin, APIView):

    class InputPostUpdateSerializer(serializers.Serializer):
        title   = serializers.CharField(max_length=100)
        content = serializers.CharField(max_length=1000)
        # file    = serializers.CharField(max_length=1000)
    
    class OutPutPostUpdateSerializer(serializers.ModelSerializer):
        author  = serializers.SerializerMethodField("get_author")
        url     = serializers.SerializerMethodField("get_url")

        class Meta:
            model = Post
            fields = ("id", "url", "title", "content", "author")

        def get_author(self, post) -> Optional[str]:
            return post.author.username

        def get_url(self, post) -> Optional[str]:
            request = self.context.get("request")
            path    = reverse("api:blog:post_detail", args=(post.id, post.slug,))
            return request.build_absolute_uri(path) if request else None
        
    @extend_schema(
        request     = InputPostUpdateSerializer,
        responses   = OutPutPostUpdateSerializer,
    )
    def post(self, request, id):
        serializer = self.InputPostUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(data={"id": file.id, "url": file.url}, status=status.HTTP_201_CREATED)
        try:
            query = post_update(
                user    = request.user,
                title   = serializer.validated_data.get("title"),
                content = serializer.validated_data.get("content"),
                id      = id,                
            )
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(self.OutPutPostUpdateSerializer(query, context={"request":request}).data)
        # return Response(status=status.HTTP_204_NO_CONTENT)

class PostDeleteApi(ApiAuthMixin, APIView):
    @extend_schema(request=None,responses=None)
    def delete(self, request, id):

        try:
            post_delete(user=request.user, id=id)
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        return Response(status=status.HTTP_204_NO_CONTENT)