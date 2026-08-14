from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from apps.workspaces.serializers import UserMiniSerializer

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
  author = UserMiniSerializer(read_only=True)
  
  class Meta:
    model = Comment
    fields = ['id', 'author', 'content', 'created_at']

class CardSerializer(serializers.ModelSerializer):
  assignee = UserMiniSerializer(read_only=True)
  comments = CommentSerializer(many=True, read_only=True)
  
  class Meta:
    model = Card
    fields = [
    'id', 'title', 'description', 'assignee',
    'position', 'priority', 'due_date',
    'comments', 'created_at', 'updated_at'
    ]

class ListSerializer(serializers.ModelSerializer):
  cards = CardSerializer(many=True, read_only=True)
  
  class Meta:
    model = List
    fields = ['id', 'name', 'position', 'cards', 'created_at']

class BoardListSerializer(serializers.ModelSerializer):
  workspace_name = serializers.CharField(source='workspace.name', read_only=True)
  list_count = serializers.IntegerField(source='lists.count', read_only=True)
  
  class Meta:
    model = Board
    fields = ['id', 'name', 'workspace_name', 'list_count', 'created_at']

class BoardDetailSerializer(serializers.ModelSerializer):
  workspace_name = serializers.CharField(source='workspace.name', read_only=True)
  lists = ListSerializer(many=True, read_only=True)
  
  class Meta:
    model = Board
    fields = ['id', 'name', 'description', 'workspace_name', 'lists', 'created_at', 'updated_at']

class CardMoveSerializer(serializers.Serializer):
  list_id = serializers.IntegerField()
  position = serializers.IntegerField()