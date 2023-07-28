from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from dp.api.mixins import ApiAuthMixin

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class LoginJwtApi(TokenObtainPairView):
    class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
        def validate(self, attrs):
            data = super().validate(attrs)
            # refresh = self.get_token(self.user)

            data['roles'] = self.user.groups.values_list('id', flat=True)
            return data

    serializer_class = MyTokenObtainPairSerializer
        
