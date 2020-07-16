from django.shortcuts import get_object_or_404

from rest_framework import viewsets, generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import User, Comment, Group, Follow, Post
from .serializers import PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer
from .permissions import AuthorOrReadOnly


class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorOrReadOnly,)
    filterset_fields = ['group',]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class FollowList(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username']
    
    def perform_create(self, serializer):
        try:
            following = User.objects.get(
                username=self.request.data.get('following'))
        except User.DoesNotExist:
            raise ValidationError(serializer.errors, status.HTTP_404_NOT_FOUND)
        if Follow.objects.filter(user=self.request.user, following=following).exists():
            raise ValidationError(serializer.errors, status.HTTP_400_BAD_REQUEST)
        if self.request.user == following:
            raise ValidationError(serializer.errors, status.HTTP_400_BAD_REQUEST)
        serializer.save(user=self.request.user, following=following)
        return Response(serializer.data, status.HTTP_201_CREATED)

 