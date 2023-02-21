import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = {'SECRET_KEY': os.getenv('SECRET_KEY'), }

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'users',
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

TEMPLATES_DIR = BASE_DIR / 'templates'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': os.getenv('DB_ENGINE', default="django.db.backends.postgresql"),
#         'NAME': os.getenv('DB_NAME', default="postgres"),
#         'USER': os.getenv('POSTGRES_USER', default="postgres"),
#         'PASSWORD': os.getenv('POSTGRES_PASSWORD', default="postgres"),
#         'HOST': os.getenv('DB_HOST', default="db"),
#         'PORT': os.getenv('DB_PORT', default="5432")
#     }
# }

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


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"

EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'

DEFAULT_FROM_EMAIL = 'admin@foodgram.cook'

# Constant values
LENG_DATA_USER = 150 #Постоянная длины данных пользователя (Имя, Фамилия, Ник)
LENG_EMAIL = 254 #Постоянная длины email пользователя
LENG_MAX = 200 #Поятонная длины рецепта
LENG_COLOR = 7 #Постоянная длины цвета
INGREDIENT_MIN_AMOUNT = 1 #Минимальное значение ингредиента
COOKING_TIME_MIN_VALUE = 1 #Минимальное значение время приготовления

#Regular expressions
USERNAME_REGEX = r'[\w\.@+-]+'
COLOR_REGEX = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'

# Notifications
NOT_ALLOWED_ME = ('Нельзя создать пользователя с '
                  'именем: << {username} >> - это имя запрещено!')
NOT_ALLOWED_CHAR_MSG = ('{chars} недопустимые символы '
                        'в имени пользователя {username}.')
NOT_COLOR_HEX = 'Введенное значение не является цветом в формате HEX'
COOKING_TIME_MIN_ERROR = (
    'Время приготовления не может быть меньше одной минуты!'
)
INGREDIENT_MIN_AMOUNT_ERROR = (
    'Количество ингредиентов не может быть меньше {min_value}!'
)
SLUG_NOTIFICATION = ("Укажите адрес для страницы тэга. "
                     "Используйте только латиницу, цифры, дефисы "
                     "и знаки подчёркивания")

