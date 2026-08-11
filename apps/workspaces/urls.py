from django.urls import path
from . import views

urlpatterns = [
  path('workspaces/', views.WorkspaceListView.as_view(), name='workspace-list'),
  path('workspaces/<slug:slug>/', views.WorkspaceDetailView.as_view, name='workspace-detail'),
  path('workspaces/<slug:slug>/members/', views.workspace_members, name='workspace-members')
]