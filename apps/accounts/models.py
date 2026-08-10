from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import *

class User(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(_('email address') ,unique=True)
  first_name = models.CharField(_('first name'), max_length=150, blank=True)
  last_name = models.CharField(_('last name'), max_length=150, blank=True)

  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_verified = models.BooleanField(default=False)

  date_joined = models.DateTimeField(default=timezone.now())
  last_login = models.DateTimeField(blank=True, null=True)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name']

  class Meta:
    db_table= 'users'
    verbose_name= _('user')
    verbose_name_plural= _("users")

  def __str__(self):
    return self.email

  def get_full_name(self):
    return f"{self.first_name} {self.last_name}".strip()

  def get_short_name(self):
    return self.first_name
