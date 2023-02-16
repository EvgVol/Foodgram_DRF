from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username, username_me


class User(AbstractUser):
    """Модель пользователя."""

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name', 
    )

    username = models.CharField(
        'Уникальный юзернейм',
        validators=(validate_username, username_me),
        max_length=settings.LENG_DATA_USER,
        unique=True,
        blank=False,
        null=False,
        help_text=f'Набор символов не более {settings.LENG_DATA_USER}.'
                  'Только буквы, цифры и @/./+/-/_',
        error_messages={
            'unique': "Пользователь с таким именем уже существует!",
        },
    )

    first_name = models.CharField(
        'Имя',
        max_length=settings.LENG_DATA_USER,
        blank=False,
        null=False,
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=settings.LENG_DATA_USER,
        blank=False,
        null=False,
        help_text=f'Набор символов не более {settings.LENG_DATA_USER}.'
    )

    email = models.EmailField(
        'Электронная почта',
        max_length=settings.LENG_EMAIL,
        unique=True,
        blank=False,
        null=False,
        help_text=f'Набор символов не более {settings.LENG_DATA_USER}.'
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=max(len(role) for role, _ in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email',
            )
        ]

    def __str__(self):
        return f'{self.username} {self.email}'
