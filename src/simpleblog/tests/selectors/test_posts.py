import pytest
from simpleblog.post.selectors import article_list, article_detail


@pytest.mark.django_db
def test_article_list(post1):
    a = article_list()
    if post1.is_online:
        assert a.get() == post1
    if not post1.is_online:
        assert a.get() != post1

@pytest.mark.django_db
def test_article_detail(post1):
    a = article_detail(id=1, slug=post1.slug)

    if post1.is_online:
        assert a.title == post1.title
        assert a.slug == post1.slug
        assert a.content == post1.content

    if not post1.is_online:
        assert a.title != post1.title
        assert a.slug != post1.slug
        assert a.content != post1.content
