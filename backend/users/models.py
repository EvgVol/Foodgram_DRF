from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    """Модель пользователя."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

    username = models.CharField(
        'Уникальный юзернейм',
        validators=(validate_username,),
        max_length=settings.LENG_DATA_USER,
        unique=True,
        blank=False,
        null=False,
        help_text=settings.USERNAME_VALUE,
        error_messages={'unique': settings.UNIQUE_USERNAME},
    )

    first_name = models.CharField(
        'Имя',
        max_length=settings.LENG_DATA_USER,
        blank=False,
        null=False,
        help_text=settings.LIMITED_NUMBER_OF_CHARACTERS
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=settings.LENG_DATA_USER,
        blank=False,
        null=False,
        help_text=settings.LIMITED_NUMBER_OF_CHARACTERS
    )

    email = models.EmailField(
        'Электронная почта',
        max_length=settings.LENG_EMAIL,
        unique=True,
        blank=False,
        null=False,
        help_text=settings.LIMITED_NUMBER_OF_CHARACTERS
    )

    password = models.CharField(
        'Пароль',
        max_length=settings.LENG_DATA_USER,
        help_text=settings.LIMITED_NUMBER_OF_CHARACTERS,
        blank=False,
        null=False
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username} {self.email}'


class Follow(models.Model):
    """Модель подписчика."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('user',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            ),
            models.CheckConstraint(
                check=~models.Q(author=models.F('user')),
                name='no_self_follow'
            )
        ]

    def __str__(self):
        return f'Пользователь {self.user} подписан на {self.author}'
