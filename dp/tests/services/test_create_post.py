import pytest
from dp.blog.services.post import post_create


@pytest.mark.django_db
def test_create_post(user2, user1, subscription1, profile1, post1):
    a = post_create(user = user1, title="pooo", content="CCCContent", image_id=0)

    assert a.author     == user1
    assert a.title      == "pooo"
    assert a.content    == "CCCContent"

