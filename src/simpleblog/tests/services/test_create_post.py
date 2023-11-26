import pytest
from simpleblog.post.services import post_create
from simpleblog.contact.services import contact_create


@pytest.mark.django_db
def test_create_post(user1, post1):
    a = post_create(user = user1, title=post1.title, content=post1.content, is_online=post1.is_online)

    assert a.author == user1
    assert a.title == post1.title
    assert a.content == post1.content
    assert a.is_online == post1.is_online

@pytest.mark.django_db
def test_create_contact(contact1):
    a = contact_create(email = contact1.email, name=contact1.name, content=contact1.content)

    assert a.email == contact1.email
    assert a.name == contact1.name
    assert a.content == contact1.content