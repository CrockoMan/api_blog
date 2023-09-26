from rest_framework import permissions


class AuthorOrReadOnlyPermission(permissions.BasePermission):
    """Проверка на права доступа."""

    def has_object_permission(self, request, view, obj):
        """Проверка на авторизацию пользователя."""
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
