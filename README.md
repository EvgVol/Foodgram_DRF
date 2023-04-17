# Foodgram - продуктовый помощник
[![Foodgram](https://github.com/evgvol/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/evgvol//foodgram-project-react/actions/workflows/foodgram_workflow.yml)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)
[![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![codecov](https://codecov.io/gh/EvgVol/foodgram-project-react/branch/master/graph/badge.svg?token=FKKAKXU90C)](https://codecov.io/gh/EvgVol/foodgram-project-react)

Дипломная работа по специальности Python-разработчик курса Яндекс.Практикум. Данная работа является заключительным этапом обучения. *
В данной работе разработан бэкенд проекта согласно спецификации API. В репозитории есть папки frontend, backend, infra, tests:
* В папке `frontend` — файлы, необходимые для сборки фронтенда приложения. 
  ###### Одностраничное приложение на фреймворке [React](https://ru.reactjs.org/), предоставлен [Яндекс.Практикумом](https://practicum.yandex.ru/). 
* В папке `infra` — конфигурационные файлы nginx и docker-compose.yml, необходимые для сборки всего проекта.
* В папке `backend` — файлы, необходимые для сборки бэкенд приложения.
* В папке `tests` — файлы, необходимые для тестирования бэкенд приложения.
 
# Descriptions
Service for publishing and sharing recipes.
Authorized users can subscribe to their favorite authors, add recipes to their favorites and shopping list, and download the shopping list. Unregistered users have access to registration, authorization, and viewing other users' recipes.

#

## Подготовка сервера

```bash
# В Settings - Secrets and variables создаем переменный с вашими данными
# Это необходимо для работы с CI/CD, DockerHub, GitHub
SECRET_KEY #'< секретный ключ >'
DEBUG #False
ALLOWED_HOSTS #'127.0.0.1, .localhost, 011.222.333.444' - адрес вашего сервера
DB_ENGINE #django.db.backends.postgresql
DB_NAME #postgres
POSTGRES_USER #postgres
POSTGRES_PASSWORD #postgres
DB_HOST #db
DB_PORT #5432
MODE #production
HOST #011.222.333.444
USER #admin
PASSWORD #password
SSH_KEY #Приватный ключ
DOCKER_USERNAME #Логин от докера
DOCKER_PASSWORD #Пароль от докера

#для использование базы данных SQLite3 укажите: MODE=dev
```

Все действия мы будем выполнять в Docker, docker-compose как на локальной машине так и на сервере ВМ Yandex.Cloud.
Предварительно установим на ВМ в облаке необходимые компоненты для работы:

*1. Подключитесь к своему серверу*

```bash
ssh admin@011.222.333.444
# admin: имя пользователя, под которым будет выполнено подключение к серверу
# 011.222.333.444: IP-адрес сервера 
```

*2. Первым делом обновите существующий список пакетов:*
```bash
sudo apt update
```

*3. Теперь обновите установленные в системе пакеты и установите обновления безопасности: на ваш сервер была установлена система из внутреннего репозитория Яндекс.Облака, и неизвестно, когда она обновлялась. Доверяй, но обновляй:*
```bash
sudo apt upgrade -y
```

*3. Установите на свой сервер Docker:*
```bash
sudo apt install docker.io
```

*4. Следующая команда загружает версию 1.26.0 и сохраняет исполняемый файл в каталоге /usr/local/bin/docker-compose, в результате чего данное программное обеспечение будет глобально доступно под именем docker-compose:*
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

*5. Затем необходимо задать правильные разрешения, чтобы сделать команду docker-compose исполняемой:*
```bash
sudo chmod +x /usr/local/bin/docker-compose
```

*6. Чтобы проверить успешность установки, запустите следующую команду:*
```bash
docker-compose --version
# Вывод будет выглядеть следующим образом:
#docker-compose version 1.26.0, build 8a1c60f6
```

*6. Скопируйте файлы docker-compose.yaml и nginx/default.conf из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно.:*
```bash
#Эти файлы нужно скопировать из директории infra локальной машины
scp docker-compose.yml nginx.conf admin@011.222.333.444:/home/admin/
```
## Запуск

Комманда git push является триггером workflow проекта. При выполнении команды git push запустится набор блоков комманд jobs (см. файл [foodgram_workflow.yml](https://github.com/evgvol/foodgram-project-react/actions/workflows/foodgram_workflow.yml)). Последовательно будут выполнены следующие блоки:

**tests** - тестирование проекта на соответствие PEP8.

**build_and_push_to_docker_hub** - при успешном прохождении тестов собирается образ (image) для docker контейнера и отправлятеся в DockerHub

**deploy** - после отправки образа на DockerHub начинается деплой проекта на сервере.

После выполнения вышеуказанных процедур необходимо установить соединение с сервером:

```bash
ssh admin@011.222.333.444
```

Выполните по очереди команды:

```bash
sudo docker-compose exec backend python manage.py migrate
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
sudo docker-compose exec backend python manage.py importcsv
```

Теперь проект доступен по адресу http://011.222.333.444/. 

#

## Документация к API   
Чтобы открыть документацию локально, запустите сервер и перейдите по ссылке:
[http://localhost/api/docs/](http://localhost/api/docs/) или воспользуйтесь докой на моей сервере: [REDOC](http://130.193.41.225/api/docs/)

#  

## Покрытие тестами

![codecov](https://codecov.io/gh/EvgVol/foodgram-project-react/branch/master/graphs/sunburst.svg?token=FKKAKXU90C)


</b></details>
<details>
<summary>Что нужно сделать чтобы установить badge покрытие проекта тестами? </summary><br><b>

* #### 1. Регистрируйтесь на сервисе: [codecov.io](https://codecov.io)


* #### 2. Настраиваем интеграцию, добавляем шаг для отправки данных на сервис
  #### Добавляем в секреты данного репозитория CODECOV_TOKEN
  #### Ниже указан код который неободимо добавить в foodgram_workflow.yml (более полный пример см. [здесь](https://github.com/codecov/codecov-action#usage)):
```bash
    - name: Upload coverage reports to Codecov
      uses: codecov/codecov-action@v2
      with:
        token: ${{ secrets.CODECOV_TOKEN }}
        files: ./coverage.xml
        flags: pytest
        name: foodgram-pytest-cov
        env_vars: OS,PYTHON
        fail_ci_if_error: true
        verbose: true
```

* #### 3. Как только сделаете pull request, можно получить анализ покрытия тестами на сервисе [codecov.io](https://codecov.io)


</b></details>



#            


|Автор проекта|[Евгений Волочек](https://github.com/EvgVol)|
|---|---|
|Ревьюер|[Евгений Салахутдинов](https://github.com/EugeneSal)|
