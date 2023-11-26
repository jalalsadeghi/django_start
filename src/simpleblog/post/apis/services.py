from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from drf_spectacular.utils import extend_schema
from django.urls import reverse

from simpleblog.api.mixins import ApiAuthMixin

from simpleblog.post.models import  Article
from simpleblog.post.services import post_create


class CreateArticleApi(ApiAuthMixin, APIView):

    class InputPostSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=100)
        content = serializers.CharField(max_length=1000)
        is_online = serializers.BooleanField(default=True)


    class OutPutPostSerializer(serializers.ModelSerializer):
        author = serializers.SerializerMethodField("get_author")
        url = serializers.SerializerMethodField("get_url")

        class Meta:
            model = Article
            fields = ("id", "title", "slug", "author", "url",)

        def get_author(self, post):
            return post.author.username

        def get_url(self, post):
            request = self.context.get("request")
            path = reverse("api:post:post_detail", args=(post.id, post.slug,))
            return request.build_absolute_uri(path)

    @extend_schema(
        responses=OutPutPostSerializer,
        request=InputPostSerializer,
    )
    def post(self, request):
        serializer = self.InputPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            query = post_create(
                user=request.user,
                title=serializer.validated_data.get("title"),
                content=serializer.validated_data.get("content"),
                is_online=serializer.validated_data.get("is_online"),
            )
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(self.OutPutPostSerializer(query, context={"request": request}).data)