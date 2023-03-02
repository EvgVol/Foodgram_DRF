from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка Пользователей."""

    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'count_followers',
        'count_recipes',
    )
    readonly_fields = ('count_followers', 'count_recipes')
    list_filter = ('username', 'email',)
    search_fields = ('username', 'email')

    @admin.display(description='Количество подписчиков')
    def count_followers(self, obj):
        """Получаем количество подписчиков."""
        return obj.follower.count()

    @admin.display(description='Количество рецептов')
    def count_recipes(self, obj):
        """Получаем количество подписчиков."""
        return obj.recipes.count()


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Админка подписчика."""

    list_display = ('user', 'author')
    list_filter = ('user', 'author')
    search_fields = ('user', 'author')
