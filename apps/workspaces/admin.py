from django.contrib import admin
from .models import *

class MemberInline(admin.TabularInline):
  model = Member
  extra = 1
  fields = ['user', 'role']

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
  list_display= ['name', 'slug', 'created_at', 'owner']
  list_filter= ['created_at']
  search_fields= ['name', 'description']
  prepopulated_fields= {'slug': ('name', )}
  inlines= [MemberInline]

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
  list_display = ['user', 'workspace', 'joined_at', 'role']
  list_filter= ['role', 'joined_at']
  search_fields= ['user__email', 'workspace__name']