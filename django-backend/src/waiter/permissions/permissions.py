from rest_framework import permissions


class IsAuthenticatedAndAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Разрешение только аутентифицированным пользователям
        if not request.user.is_authenticated:
            return False
        # Разрешение на чтение всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешение только администраторам на создание и изменение
        return request.user.groups.filter(name='Admins').exists()