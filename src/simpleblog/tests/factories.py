import factory
import random

from datetime import datetime
from django.utils.text import slugify
from django.contrib.auth.models import User

from simpleblog.post.models import Article
from simpleblog.contact.models import Contact
from simpleblog.tests.utils import faker


class BaseUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Iterator(['frcom', 'itcom', 'escom'])
    email = factory.Iterator(['fr@gmail.com', 'it@gmail.com', 'es@gmail.com'])
    password = factory.PostGenerationMethodCall('set_password', 'adm1n')

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    title = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
    content = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
    slug = slugify(title)
    created_at = faker.date_between_dates(date_start=datetime(2015,1,1),
                                          date_end=datetime(2019,12,31))
    updated_at = created_at
    author = factory.SubFactory(BaseUserFactory)
    is_online = True        #random.choice([True, False])

class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contact

    email = factory.Iterator(['fr@gmail.com', 'it@gmail.com', 'es@gmail.com'])
    name = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
    content = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
    created_at = faker.date_between_dates(date_start=datetime(2015,1,1),
                                          date_end=datetime(2019,12,31))
    updated_at = created_at
