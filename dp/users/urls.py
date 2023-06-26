from django.urls import path
from .apis import LoginJwtApi, ProfileApi, RegisterApi


urlpatterns = [
    path('register/', RegisterApi.as_view(),name="register"),
    path('login/', LoginJwtApi.as_view(),name="login"),
    path('profile/', ProfileApi.as_view(),name="profile"),
]
