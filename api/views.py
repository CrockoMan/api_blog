from rest_framework import viewsets, serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404

from api.serializers import PostSerializer, GroupSerializer, CommentSerializer
from posts.models import Post, Group


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """(GET): получаем список всех групп."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    """(GET, POST): получаем список всех постов или создаём новый пост."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        '''Создание нового поста.'''
        return serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_destroy(serializer)


class CommentViewSet(viewsets.ModelViewSet):
    """(GET, POST): получаем список всех постов или создаём новый пост."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    post = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        '''Выбор комментариев к посту.'''
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        '''Создание комментария к посту.'''
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_destroy(serializer)
