from dp.blog.models import Post, Subscription
from dp.users.models import BaseUser, Profile

from django.db import transaction
from django.db.models import QuerySet
from django.utils.text import slugify
from django.core.cache import cache


def count_follower(*, user: BaseUser) -> int:
    return Subscription.objects.filter(target=user).count()


def count_following(*, user: BaseUser) -> int:
    return Subscription.objects.filter(subscriber=user).count()

def count_posts(*, user: BaseUser) -> int:
    return Post.objects.filter(author=user).count()

def cache_profile(*, user: BaseUser) -> None:
    profile = {
            "posts_count": count_posts(user=user),
            "subscribers_count": count_follower(user=user),
            "subscriptions_count": count_following(user=user),
            }
    cache.set(f"profile_{user}", profile, timeout=None)

def subscribe(*, user: BaseUser, email: str) -> QuerySet[Subscription]:
    target = BaseUser.objects.get(email=email)
    sub = Subscription(subscriber=user, target=target)
    sub.full_clean()
    sub.save()
    cache_profile(user=user)
    return sub


def unsubscribe(*, user: BaseUser, username: str) -> dict:
    target = BaseUser.objects.get(username=username)
    Subscription.objects.get(subscriber=user, target=target).delete()
    cache_profile(user=user)

@transaction.atomic
def post_create(*, user:BaseUser, title:str, content:str) -> QuerySet[Post]:
    post = Post.objects.create(
        author=user, title=title, content=content, slug=slugify(title)
    )

    cache_profile(user=user)
    return post

@transaction.atomic
def post_update(*, user:BaseUser, id:int, title:str, content:str) -> QuerySet[Post]:
    Post.objects.filter(author=user, id=id).update(title=title, content=content, slug=slugify(title))
    post = Post.objects.get(
        author=user, title=title, content=content, slug=slugify(title)
    )
    return post

def post_delete(*, user:BaseUser, id:int):
    post = Post.objects.get(author=user, id=id).delete()

    cache_profile(user=user)
    return post
