from django.urls import path
from .apis import ProfileApi, RegisterApi,LoginJwtApi


urlpatterns = [
    path('register/', RegisterApi.as_view(),name="register"),
    path('login/', LoginJwtApi.as_view(),name="login"),
    path('profile/', ProfileApi.as_view(),name="profile"),
]
