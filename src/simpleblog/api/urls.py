from django.urls import path, include

urlpatterns = [
    path('auth/', include(('simpleblog.authentication.urls', 'auth'))),
    path('post/', include(('simpleblog.post.urls', 'post'))),
    path('contact/',   include(('simpleblog.contact.urls', 'contact'))),
]
