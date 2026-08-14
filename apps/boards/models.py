from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

from apps.workspaces.models import Workspace

class Board(models.Model):
  workspace = models.ForeignKey(
    Workspace,
    on_delete=models.CASCADE,
    related_name='boards'
  )

  name = models.CharField(max_length=100, unique=True)
  description = models.TextField(blank=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ['-created_at']

  def __str__(self):
    return f"{self.name} ({self.workspace.name})"

class List(models.Model):
  board = models.ForeignKey(
    Board,
    on_delete=models.CASCADE,
    related_name='lists'
  )

  name= models.CharField(max_length=100)
  position = models.PositiveIntegerField(default=0)

  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['position', '-created_at']

  def __str__(self):
    return f"{self.name} ({self.board.name})"

class Card(models.Model):
  PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High')
  ]

  list = models.ForeignKey(
    List,
    on_delete=models.CASCADE,
    related_name='cards'
  )

  assignee = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='assigned_cards',
  )

  title = models.CharField(max_length=100)
  description= models.TextField()
  position= models.PositiveIntegerField(default=0)
  priority= models.CharField(
    max_length=10,
    choices=PRIORITY_CHOICES,
    default='medium'
  )
  due_date = models.DateTimeField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ['position', '-created_at']

  def __str__(self):
    return self.title

class Comment(models.Model):
  card = models.ForeignKey(
    Card,
    on_delete=models.CASCADE,
    related_name='comments'
  )

  author = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='comments',
  )

  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['-created_at']

  def __str__(self):
    return f"Comment by {self.author.email} on {self.card.title}"