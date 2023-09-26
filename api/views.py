from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from api.permissions import AuthorOrReadOnlyPermission
from api.serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """(GET): получаем список всех групп."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    """(GET, POST): получаем список всех постов или создаём новый пост."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, AuthorOrReadOnlyPermission,)

    def perform_create(self, serializer):
        '''Создание нового поста.'''
        return serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """(GET, POST): получаем список всех постов или создаём новый пост."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, AuthorOrReadOnlyPermission,)

    def get_one_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        '''Выбор комментариев к посту.'''
        return self.get_one_post().comments.all()

    def perform_create(self, serializer):
        '''Создание комментария к посту.'''
        serializer.save(author=self.request.user, post=self.get_one_post())
