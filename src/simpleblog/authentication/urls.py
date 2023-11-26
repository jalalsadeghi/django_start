from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from simpleblog.authentication.api import LoginJwtApi

urlpatterns = [
        path('jwt/', include(([
            path('login/',   LoginJwtApi.as_view(),name="login"),
            path('refresh/', TokenRefreshView.as_view(),name="refresh"),
            path('verify/',  TokenVerifyView.as_view(),name="verify"),
            # path('logout/',  LogoutApi.as_view(), name='logout'),
            ], "jwt")),),
]
