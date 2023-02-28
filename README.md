# Foodgram
<!-- [![Foodgram](https://github.com/evgvol/< название-проекта >/actions/workflows/< название-файла >.yml/badge.svg)](https://github.com/evgvol/< название-проекта >/actions/workflows/< название-файла >.yml) -->

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)
[![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

## Описание
Cервис для публикаций и обмена рецептами.

Авторизованные пользователи могут подписываться на понравившихся авторов, добавлять рецепты в избранное, в покупки, скачивать список покупок. Неавторизованным пользователям доступна регистрация, авторизация, просмотр рецептов других пользователей.

## Как запустить
Из корневой папки выполните:
```
docker-compose up --build
```
Узнайте id существующих контейнеров
```
docker container ls
```
Скопируйте id web-контейнера и войдите в него
```
docker exec -it <CONTAINER ID> sh
```
Сделайте миграцию БД и сбор статики
```
python manage.py migrate
python manage.py collectstatic
```
## Окружение
Для хранения важных данных использован .env файл. Файл добавлен в .gitignore, чтобы исключить попадание в Git.
Для запуска сайта необходимо в папке backend создать .env файл со следующими переменными:
DEBUG
SECRET_KEY
ALLOWED_HOSTS
DB_ENGINE
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
MODE=dev

## Документация к API
Чтобы открыть документацию локально, запустите сервер и перейдите по ссылке:
[http://127.0.0.1/api/docs/](http://127.0.0.1/api/docs/)
