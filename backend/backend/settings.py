from pathlib import Path

from decouple import Csv, config
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-284jnm=8n5j4^#kfmroc%=@nj+qke7#n$gw54y0iba1-&##f(d'
)

DEBUG = config('DEBUG', cast=bool, default=True)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    cast=Csv(),
    default='127.0.0.1'
)

MODE = config('MODE', cast=str, default='dev')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'djoser',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'api',
    'users',
    'recipes',
    'colorfield',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

if MODE == 'dev':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': config('DB_ENGINE'),
            'NAME': config('DB_NAME'),
            'USER': config('POSTGRES_USER'),
            'PASSWORD': config('POSTGRES_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT')
        }
    }

AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Samara'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 6,
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'HIDE_USER': 'True',
    'SERIALIZERS': {
        'current_user': 'api.serializers.UsersSerializer',
    },
    'PERMISSIONS': {
        'user': ['djoser.permissions.CurrentUserOrAdminOrReadOnly'],
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"

EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'

DEFAULT_FROM_EMAIL = 'admin@foodgram.cook'

# Далее вынесены постоянные которые нужны для работы проекта
# ----------------------------------------------------------------------------
# Constant values
LENG_DATA_USER = 150
LENG_EMAIL = 254
LENG_MAX = 200
LENG_COLOR = 7
RECIPES_LIMIT = 3
INGREDIENT_MIN_AMOUNT = 1
COOKING_TIME_MIN_VALUE = 1
INCORRECT_LAYOUT = str.maketrans(
    'qwertyuiop[]asdfghjkl;\'zxcvbnm,./',
    'йцукенгшщзхъфывапролджэячсмитьбю.'
)
# ----------------------------------------------------------------------------
#Regular expressions
USERNAME_REGEX = r'[\w\.@+-]+'
COLOR_REGEX = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
# ----------------------------------------------------------------------------
# Notifications
MAX_NUMBER_OF_CHARACTERS = f'Количество символов не более {LENG_MAX}.'
LIMITED_NUMBER_OF_CHARACTERS = f'Набор символов не более {LENG_DATA_USER}'
NOT_ALLOWED_ME = ('Нельзя создать пользователя с '
                  'именем: << {username} >> - это имя запрещено!')
NOT_ALLOWED_CHAR_MSG = ('{chars} недопустимые символы '
                        'в имени пользователя {username}.')
DUBLICAT_USER = 'Вы уже подписаны на этого пользователя!'
SELF_FOLLOW = 'Вы не можете подписаться на самого себя!'
NOT_COLOR_HEX = 'Введенное значение не является цветом в формате HEX'
COLOR_NO_UNIQUE = 'Такой цвет уже существует!'
HELP_CHOISE_COLOR = 'Для выбора цвета воспользуйтесь цветовой панелью.'
COOKING_TIME_MIN_ERROR = (
    'Время приготовления не может быть меньше одной минуты!'
)
INGREDIENT_MIN_AMOUNT_ERROR = (
    'Количество ингредиентов не может быть меньше {min_value}!'
)
SLUG_NOTIFICATION = ('Укажите адрес для страницы тэга. '
                     'Используйте только латиницу, цифры, дефисы '
                     'и знаки подчёркивания')
INGREDIENT_DUBLICATE_ERROR = 'Ингредиенты не могут повторяться!'
TAG_ERROR = 'Рецепт не может быть без тегов!'
TAG_UNIQUE_ERROR = 'Теги должны быть уникальными!'
RECIPE_IN_FAVORITE = 'Вы уже добавили рецепт в избранное.'
ALREADY_BUY = 'Вы уже добавили рецепт в список покупок.'
UNIQUE_USERNAME = 'Пользователь с таким именем уже существует!'
USERNAME_VALUE = (f'Набор символов не более {LENG_DATA_USER}.'
                  'Только буквы, цифры и @/./+/-/_')
# ----------------------------------------------------------------------------
