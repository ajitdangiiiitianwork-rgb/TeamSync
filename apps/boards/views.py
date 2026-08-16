from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count

from .models import Board, List, Card, Comment
from .serializers import (
    BoardListSerializer,
    BoardDetailSerializer,
    CardMoveSerializer,
)
from apps.workspaces.models import Member

class IsBoardWorkspaceMember(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    return Member.objects.filter(
      workspace = obj.workspace,
      user = request.user,
    ).exists()

class BoardListView(generics.ListCreateAPIView):
  def get_serializer_class(self):
    if self.request.method == 'POST':
      return BoardCreateSerializer
    return BoardListSerializer

  def get_queryset(self):
    return  Board.objects.filter(
      workspace__members__user = self.request.user
    )

class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = BoardDetailSerializer

  permission_classes = [
    permissions.IsAuthenticated,
    IsBoardWorkspaceMember,
  ]

  def get_queryset(self):
    return Board.objects.filter(
      workspace__members__user= self.request.user
    )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def move_card(request, pk):
  card = get_object_or_404(Card, pk=pk)
  workspace = card.list.board.workspace
  if not Member.objects.filter(workspace=workspace, user=request.user).exists():
    raise PermissionError("Not a member of this workspace")

  new_list_id = request.data.get('list_id')
  new_position = request.data.get('position')

  new_list = get_object_or_404(List, pk=new_list_id)

  if new_list.board != card.list.board :
    raise PermissionError({'Error' : 'Cannot move to a different board'}, status = 400)

  card.list = new_list
  card.position = new_position
  card.save()

  return Response({'status' : 'moved', 'card' : card.title})