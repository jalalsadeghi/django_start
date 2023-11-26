from django.urls import path

from simpleblog.contact.apis import ContactApi


urlpatterns = [
    path("contact/", ContactApi.as_view(), name="contact"),
]