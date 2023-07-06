from django.db import models
from django.core.exceptions import ValidationError
from dp.common.models import BaseModel
from dp.users.models import BaseUser
from dp.files.models import File


class Post(BaseModel):
    slug = models.SlugField(
            max_length=100,
    )
    title = models.CharField(
        max_length=100,
    )
    content = models.CharField(
        max_length=1000,
    )
    author = models.ForeignKey(
            BaseUser, 
            on_delete=models.SET_NULL,
            null=True,
    )
    image = models.ForeignKey(File,
                              on_delete=models.SET_NULL,
                              null=True,)

    def __str__(self):
        return self.slug


class Subscription(models.Model):
    subscriber = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="subs")
    target     = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="targets")

    class Meta:
        unique_together = ('subscriber', 'target')

    def clean(self):
        if self.subscriber == self.target:
            raise ValidationError({"subscriber": ("subscriber cannot be equal to target")})

    def __str__(self):
        return f"{self.subscriber.email}- {self.target.email}"
