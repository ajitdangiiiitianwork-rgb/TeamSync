from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Workspace(models.Model):
  name= models.CharField(max_length=255)
  slug= models.SlugField(max_length=255, unique=True, blank=True)
  description= models.TextField()
  owner= models.ForeignKey(
    User,
    related_name='owned_workspaces',
    on_delete=models.CASCADE,
  )

  created_at= models.DateTimeField(auto_now_add=True)
  updated_at= models.DateTimeField(auto_now=True)

  class Meta:
    ordering= ['-created_at']

  def __str__(self):
    return self.name

class Member(models.Model):
  ROLE_CHOICES= [
    ('admin', 'Admin'),
    ('editor', 'Editor'),
    ('viewer', 'Viewer')
  ]

  workspace= models.ForeignKey(
    Workspace,
    on_delete=models.CASCADE,
    related_name='members'
  )

  user= models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='memberships'
  )

  role= models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer')

  joined_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together= ['workspace', 'user']
    ordering= ['-joined_at']

  def __str__(self):
    return f"{self.user.email} - {self.workspace} ({self.role})"
