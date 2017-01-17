from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    email = models.EmailField(_('email address'), blank=False, null=False, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Customer(models.Model):
    user = models.OneToOneField(User)
    stripe_customer_id = models.CharField(max_length=64)
