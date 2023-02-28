from django.core.handlers.wsgi import WSGIRequest
from rest_framework import permissions
from rest_framework.routers import APIRootView


class BanPermission(permissions.BasePermission):
    """Базовый класс разрешений с проверкой - забанен ли пользователь."""

    def has_permission(self, request: WSGIRequest, view: APIRootView):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
        )


class AuthorStaffOrReadOnly(BanPermission):
    """Разрешение на изменение только для служебного персонала и автора.
    Остальным только чтение объекта.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
            and (
                request.user == obj.author
                or request.user.is_staff
            )
        )


class IsAdminOrReadOnly(BanPermission):
    """Разрешение на создание и изменение только для админов.
    Остальным только чтение объекта.
    """
    def has_object_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
            and request.user.is_staff
        )


class OwnerUserOrReadOnly(BanPermission):
    """
    Разрешение на создание и изменение только для админа и пользователя.
    Остальным только чтение объекта.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
            and request.user == obj.author
            or request.user.is_staff
        )
