from django.urls import path, include

urlpatterns = [
    path('blog/', include(('dp.blog.urls', 'blog'))),
    path('users/', include(('dp.users.urls', 'users'))),
    path('auth/', include(('dp.authentication.urls', 'auth'))),
]
