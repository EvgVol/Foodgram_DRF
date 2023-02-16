import re

from django.core.exceptions import ValidationError


USERNAME_REGEX = r'[\w\.@+-]+'
NOT_ALLOWED_ME = ('Нельзя создать пользователя с '
                  'именем: << {username} >> - это имя запрещено!')
NOT_ALLOWED_CHAR_MSG = ('{chars} недопустимые символы '
                        'в имени пользователя {username}.')


def validate_username(username):
    invalid_symbols = ''.join(set(re.sub(USERNAME_REGEX, '', username)))
    if invalid_symbols:
        raise ValidationError(
            NOT_ALLOWED_CHAR_MSG.format(
                chars=invalid_symbols, username=username))
    if username == 'me':
        raise ValidationError(NOT_ALLOWED_ME.format(username=username))
    return username


def username_me(value): 
    """Проверка имени пользователя (me недопустимое имя).""" 
    if value == 'me': 
        raise ValidationError( 
            'Имя пользователя "me" не разрешено.' 
        ) 
    return value 
