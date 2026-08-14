from django.contrib import admin
from .models import Board, List, Card, Comment


class ListInline(admin.TabularInline):
    model = List
    extra = 1
    fields = ['name', 'position']


class CardInline(admin.TabularInline):
    model = Card
    extra = 1
    fields = ['title', 'assignee', 'position', 'priority']


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ['author', 'content']


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['name', 'workspace', 'created_at']
    list_filter = ['workspace', 'created_at']
    search_fields = ['name', 'description']
    inlines = [ListInline]


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ['name', 'board', 'position', 'created_at']
    list_filter = ['board']
    search_fields = ['name']
    inlines = [CardInline]


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['title', 'list', 'assignee', 'priority', 'position', 'created_at']
    list_filter = ['priority', 'list__board', 'created_at']
    search_fields = ['title', 'description']
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'card', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'author__email']