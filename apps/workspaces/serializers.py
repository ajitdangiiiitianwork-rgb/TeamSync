from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class UserMiniSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'first_name', 'last_name', 'get_full_name']

class MemberSerializer(serializers.ModelSerializer):
  user = UserMiniSerializer(read_only=True)

  class Meta:
    model = Member
    fields = ['id', 'user', 'role', 'joined_at']

class WorkspaceListSerializer(serializers.ModelSerializer):
  owner= UserMiniSerializer(read_only=True)
  member_count= serializers.IntegerField(source= 'members.count', read_only=True)
  your_role= serializers.SerializerMethodField()

  class Meta:
    model= Workspace
    fields = ['id', 'name', 'slug', 'description', 'owner', 'member_count', 'your_role', 'created_at']

  def get_your_role(self, obj):
    request = self.context.get('request')
    if request and request.user.is_authenticated:
      membership = obj.members.filter(user=request.user).first()
      if membership:
        return membership.role
    return None

class WorkspaceDetailSerializer(serializers.ModelSerializer):
  owner = UserMiniSerializer(read_only=True)
  member = MemberSerializer(read_only=True)

  class Meta:
    model= Workspace
    fields = ['id', 'name', 'slug', 'description', 'owner', 'members', 'created_at', 'updated_at']

class MemberCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Member
    fields = ['user', 'role']