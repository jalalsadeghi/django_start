from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from django.core.validators import MinLengthValidator
from .validators import number_validator, special_char_validator, letter_validator
from dp.api.mixins import ApiAuthMixin

from dp.users.models import BaseUser , Profile
from dp.users.selectors import get_profile
from dp.users.services import register 

from drf_spectacular.utils import extend_schema
from django.core.cache import cache

from typing import Optional


class ProfileApi(ApiAuthMixin, APIView):

    class OutPutProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile 
            fields = ("posts_count", "subscriber_count", "subscription_count")

        def to_representation(self, instance):
            rep = super().to_representation(instance)
            cache_profile = cache.get(f"profile_{instance.user}", {})
            if cache_profile:
                rep["posts_count"] = cache_profile.get("posts_count")
                rep["subscriber_count"] = cache_profile.get("subscribers_count")
                rep["subscription_count"] = cache_profile.get("subscriptions_count")

            return rep

    @extend_schema(responses=OutPutProfileSerializer)
    def get(self, request):
        query = get_profile(user=request.user)
        return Response(self.OutPutProfileSerializer(query, context={"request":request}).data)


class RegisterApi(APIView):

    class InputRegisterSerializer(serializers.Serializer):
        email       = serializers.EmailField(max_length=255)
        username    = serializers.CharField(max_length=20)
        password    = serializers.CharField(
                validators=[
                        number_validator,
                        letter_validator,
                        special_char_validator,
                        MinLengthValidator(limit_value=10)
                    ]
                )
        confirm_password = serializers.CharField(max_length=255)
        
        def validate_email(self, email):
            if BaseUser.objects.filter(email=email).exists():
                raise serializers.ValidationError("email Already Taken")
            return email
        
        def validate_username(self, username):
            if BaseUser.objects.filter(username=username).exists():
                raise serializers.ValidationError("username Already exists")
            return username

        def validate(self, data):
            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError("Please fill password and confirm password")
            
            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError("confirm password is not equal to password")
            return data


    class OutPutRegisterSerializer(serializers.ModelSerializer):

        token = serializers.SerializerMethodField("get_token")

        class Meta:
            model = BaseUser 
            fields = ("email", "username", "token", "created_at", "updated_at")

        def get_token(self, user) -> Optional[str]:
            data = dict()
            token_class = RefreshToken

            refresh = token_class.for_user(user)

            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)

            return data


    @extend_schema(request=InputRegisterSerializer, responses=OutPutRegisterSerializer)
    def post(self, request):
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = register(
                    email       =serializer.validated_data.get("email"),
                    username    =serializer.validated_data.get("username"),
                    password    =serializer.validated_data.get("password"),
                    )
        except Exception as ex:
            return Response(
                    f"Database Error {ex}",
                    status=status.HTTP_400_BAD_REQUEST
                    )
        return Response(self.OutPutRegisterSerializer(user, context={"request":request}).data)


