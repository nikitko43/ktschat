from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Message(models.Model):
    author = models.CharField(max_length=30)
    text = models.TextField(blank=True, null=True, default='')
    time = models.DateTimeField(auto_now=True)
    attached_file = models.FileField(blank=True, null=True, default=None)

    def __str__(self):
        return self.text


class Profile(AbstractUser):
    avatar = models.FileField(blank=True, null=True, default=None, verbose_name='Аватар')

    objects = UserManager()

    class Meta:
        db_table = 'profiles'
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')