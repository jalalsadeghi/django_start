from django.contrib import admin
from simpleblog.post.models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    list_display = ['title', 'created_at', 'is_online']