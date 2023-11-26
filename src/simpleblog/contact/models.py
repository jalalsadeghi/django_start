from django.db import models

from simpleblog.common.models import BaseModel

class Contact(BaseModel):
    email = models.EmailField(max_length=255)
    name = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.email