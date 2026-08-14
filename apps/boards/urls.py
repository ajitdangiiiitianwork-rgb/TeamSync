from django.urls import path
from . import views

urlpatterns = [
  path('boards/', views.BoardListView.as_view(), name='board-list'),
  path('boards/<int:pk>/', views.BoardDetailView.as_view(), name='board-detail'),
  path('boards/<int:pk>/move/', views.move_card, name='card-move')
]