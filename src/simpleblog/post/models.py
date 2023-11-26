from django.contrib.auth.models import User
from django.db import models

from django.db.models.signals import pre_save
from django.dispatch import receiver

from simpleblog.common.models import BaseModel


class Article(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

@receiver(pre_save, sender=Article)
def pre_save_article(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = instance.title.replace(" ", "-").lower()