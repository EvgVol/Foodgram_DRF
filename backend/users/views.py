from djoser.views import UserViewSet

from api.pagination import LimitPageNumberPagination


class CustomUserViewSet(UserViewSet):
    """Отображение пользователей."""

    pagination_class = LimitPageNumberPagination