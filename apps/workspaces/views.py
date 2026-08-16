from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Workspace, Member
from .serializers import (
    WorkspaceListSerializer,
    WorkspaceDetailSerializer,
    MemberSerializer,
    MemberCreateSerializer,
)

class IsWorkspaceMember(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    return Member.objects.filter(workspace=obj, user=request.user).exists()

class IsWorkspaceAdmin(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    membership = Member.objects.filter(workspace=obj, user=request.user).first()
    return membership is not None and membership.role == 'admin'

class WorkspaceListView(generics.ListCreateAPIView):
  permission_classes = [permissions.IsAuthenticated] 
  def get_serializer_class(self):
    if self.request.method == "POST":
      return WorkspaceDetailSerializer
    return WorkspaceListSerializer

  def get_queryset(self):
    return Workspace.objects.filter(members__user= self.request.user)

  def perform_create(self, serializer):
    # Save the workspace with current user as owner
    workspace = serializer.save(owner=self.request.user)
    
    # Automatically create a Member record for the creator
    # with admin role
    Member.objects.create(
      workspace=workspace,
      user=self.request.user,
      role='admin'
    )

class WorkspaceDetailView(generics.RetrieveUpdateDestroyAPIView):
  lookup_field = 'slug'
  serializer_class = WorkspaceDetailSerializer
  permission_classes = [
    permissions.IsAuthenticated,
    IsWorkspaceMember,  # Must be a member to even see it
  ]

  def get_queryset(self):
    return Workspace.objects.filter(members__user = self.request.user)

  def get_permissions(self):
    # For GET, use existing permissions (IsAuthenticated + IsWorkspaceMember)
    if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
      return [permissions.IsAuthenticated(), IsWorkspaceMember()]
    
    # For PUT/PATCH/DELETE, require admin
    return [permissions.IsAuthenticated(), IsWorkspaceMember(), IsWorkspaceAdmin()]

  def perform_destroy(self, instance):
    if instance.owner != self.request.user:
      raise permissions.PermissionDenied("Only the owner can delete this workspace.")
    instance.delete()

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def workspace_members(request, slug):
  # Find the workspace
  workspace = get_object_or_404(Workspace, slug=slug)
  
  # Check if current user is a member
  if not Member.objects.filter(workspace=workspace, user=request.user).exists():
    raise permissions.PermissionDenied("You are not a member of this workspace.")

  # GET branch
  if request.method == 'GET':
    members = workspace.members.all()
    serializer = MemberSerializer(members, many=True)
    return Response(serializer.data)

  # POST branch — invite member
  # Check admin
  membership = Member.objects.filter(workspace=workspace, user=request.user).first()
  if membership.role != 'admin':
    raise permissions.PermissionDenied("Only admins can invite members.")
  
  serializer = MemberCreateSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save(workspace=workspace)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)