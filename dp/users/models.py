from django.db import models
from dp.common.models import BaseModel

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

class BaseUserManager(BUM):
    def create_user(self, username, password, email, first_name, last_name, is_active=True, is_admin=False, is_superuser=False):
        if not email:
            raise ValueError("Users must have an email address")
        
        if not username:
            raise ValueError("The given username must be set")

        user = self.model(email=self.normalize_email(email.lower()),
                          username      = (username.lower()), 
                          first_name    = first_name,
                          last_name     = last_name,
                          is_active     = is_active, 
                          is_admin      = is_admin,
                          is_superuser  = is_superuser,
                          )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user
    def create_superuser(self, username, password, email):
        user = self.create_user(
            username    = username, 
            password    = password, 
            email       = email,
            first_name  = username,
            last_name   = username, 
            is_active   = True, 
            is_admin    = True,
            is_superuser= True)
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(verbose_name = "email address",
                              unique=True)
    
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name      = models.CharField(_("first name"), max_length=150, null=True, blank=True)
    last_name       = models.CharField(_("last name"), max_length=150, null=True, blank=True)

    is_active       = models.BooleanField(default=True)
    is_admin        = models.BooleanField(default=False)

    objects         = BaseUserManager()

    EMAIL_FIELD     = "email"
    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def is_staff(self):
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    posts_count = models.PositiveIntegerField(default=0)
    subscriber_count = models.PositiveIntegerField(default=0)
    subscription_count = models.PositiveIntegerField(default=0)
    bio = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.user} >> {self.bio}"
