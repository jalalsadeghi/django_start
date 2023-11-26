from django.db.models import QuerySet
from simpleblog.post.models import Article


def article_list() -> QuerySet[Article]:
    query = Article.objects.filter(is_online=True)
    return query


def article_detail(*, id: int, slug: str) -> Article:
    return Article.objects.get(id=id, slug=slug)
