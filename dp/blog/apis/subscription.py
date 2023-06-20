from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from drf_spectacular.utils import extend_schema

from dp.api.pagination import get_paginated_response, LimitOffsetPagination

from dp.blog.models import Subscription
from dp.blog.selectors.posts import get_subscribers
from dp.blog.services.post import unsubscribe, subscribe
from dp.api.mixins import ApiAuthMixin


class UnsubscribeApi(ApiAuthMixin, APIView):

    def delete(self, request, username):
        try:
            unsubscribe(user=request.user, username=username)
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeApi(ApiAuthMixin, APIView):

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class InputSubSerializer(serializers.Serializer):
        email = serializers.CharField(max_length=100)

    class OutPutSubSerializer(serializers.ModelSerializer):
        email = serializers.SerializerMethodField("get_email")

        class Meta:
            model = Subscription 
            fields = ("email",)

        def get_email(self, subscription):
            return subscription.target.email


    @extend_schema(
        responses=OutPutSubSerializer,
    )
    def get(self, request):
        user = request.user
        query = get_subscribers(user=user)
        return get_paginated_response(
                request=request,
                pagination_class=self.Pagination,
                queryset=query,
                serializer_class=self.OutPutSubSerializer,
                view=self,
                ) 

    @extend_schema(
        request=InputSubSerializer,
        responses=OutPutSubSerializer,
    )
    def post(self, request):
        serializer = self.InputSubSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            query = subscribe(user=request.user, email=serializer.validated_data.get("email"))
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        output_serilaizer = self.OutPutSubSerializer(query)
        return Response(output_serilaizer.data)

