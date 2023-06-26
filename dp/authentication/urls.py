from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
# from .api import LogoutApi

urlpatterns = [
        path('jwt/', include(([
            # path('login/',   TokenObtainPairView.as_view(),name="login"),
            path('refresh/', TokenRefreshView.as_view(),name="refresh"),
            path('verify/',  TokenVerifyView.as_view(),name="verify"),
            # path('logout/',  LogoutApi.as_view(), name='logout'),
            ], "jwt")),),
]
