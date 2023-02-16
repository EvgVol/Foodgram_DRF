import pytest
from django.contrib.auth import get_user_model

from .common import auth_client, create_users_api


class TestUserAPI:

    @pytest.mark.django_db(transaction=True)
    def test_auth_urls(self, client):
        urls = ['/api/auth/login/', '/auth/token/logout/']
        for url in urls:
            try:
                response = client.get(url)
            except Exception as e:
                assert False, f'''Страница `{url}` работает неправильно. Ошибка: `{e}`'''
            assert response.status_code != 404, f'Страница `{url}` не найдена, проверьте этот адрес в *urls.py*'
            assert response.status_code == 200, (
                f'Ошибка {response.status_code} при открытиии `{url}`. Проверьте ее view-функцию'
            )

    @pytest.mark.django_db(transaction=True)
    def test_users_not_authenticated(self, client):
        response = client.get('/api/users/')

        assert response.status_code != 404, (
            'Страница `/api/users/` не найдена, проверьте этот адрес в *urls.py*'
        )

        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/users/` без токена авторизации возвращается статус 401'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_username_not_authenticated(self, client, admin):
        response = client.get(f'/api/users/{admin.username}/')

        assert response.status_code != 404, (
            'Страница `/api/users/{username}/` не найдена, проверьте этот адрес в *urls.py*'
        )

        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/users/{username}/` без токена авторизации возвращается статус 401'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_me_not_authenticated(self, client):
        response = client.get('/api/users/me/')

        assert response.status_code != 404, (
            'Страница `/api/users/me/` не найдена, проверьте этот адрес в *urls.py*'
        )

        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/users/me/` без токена авторизации возвращается статус 401'
        )


    @pytest.mark.django_db(transaction=True)
    def test_users_get_admin(self, admin_client, admin):
        response = admin_client.get('/api/users/')
        assert response.status_code != 404, (
            'Страница `/api/users/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/users/` с токеном авторизации возвращается статус 200'
        )
        data = response.json()
        assert 'count' in data, (
            'Проверьте, что при GET запросе `/api/users/` возвращаете данные с пагинацией. '
            'Не найден параметр `count`'
        )
        assert 'next' in data, (
            'Проверьте, что при GET запросе `/api/users/` возвращаете данные с пагинацией. '
            'Не найден параметр `next`'
        )
        assert 'previous' in data, (
            'Проверьте, что при GET запросе `/api/users/` возвращаете данные с пагинацией. '
            'Не найден параметр `previous`'
        )
        assert 'results' in data, (
            'Проверьте, что при GET запросе `/api/users/` возвращаете данные с пагинацией. '
            'Не найден параметр `results`'
        )
        assert data['count'] == 1, (
            'Проверьте, что при GET запросе `/api/users/` возвращаете данные с пагинацией. '
            'Значение параметра `count` не правильное'
        )
        assert type(data['results']) == list, (
            'Проверьте, что при GET запросе `/api/users/` возвращаете данные с пагинацией. '
            'Тип параметра `results` должен быть список'
        )
        assert (
            len(data['results']) == 1
            and data['results'][0].get('username') == admin.username
            and data['results'][0].get('email') == admin.email
        ), (
            'Проверьте, что при GET запросе `/api/users/` возвращаете данные с пагинацией. '
            'Значение параметра `results` не правильное'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_get_search(self, admin_client, admin):
        url = '/api/users/'
        search_url = f'{url}?search={admin.username}'
        response = admin_client.get(search_url)
        assert response.status_code != 404, (
            'Страница `/api/users/?search={username}` не найдена, проверьте этот адрес в *urls.py*'
        )
        reponse_json = response.json()
        assert 'results' in reponse_json and isinstance(reponse_json.get('results'), list), (
            'Проверьте, что при GET запросе `/api/users/?search={username}` '
            'результаты возвращаются под ключом `results` и в виде списка.'
        )
        users_count = get_user_model().objects.filter(username=admin.username).count()
        assert len(reponse_json['results']) == users_count, (
            'Проверьте, что при GET запросе `/api/users/?search={username}` '
            'возвращается только пользователь с указанным в поиске username'
        )
        admin_as_dict = {
            'username': admin.username,
            'email': admin.email,
            'role': admin.role,
            'first_name': admin.first_name,
            'last_name': admin.last_name,
        }
        assert reponse_json['results'] == [admin_as_dict], (
            'Проверьте, что при GET запросе `/api/users/?search={username}` '
            'возвращается искомый пользователь со всеми необходимыми полями, включая `role`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_get_admin_only(self, user_client):
        url = '/api/users/'
        response = user_client.get(url)
        assert response.status_code != 404, (
            f'Страница `{url}` не найдена, проверьте этот адрес в *urls.py*'
        )
        status = 403
        assert response.status_code == status, (
            f'Проверьте, что при GET запросе `{url}` не для администратора возвращается статус {status}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_post_admin(self, admin_client, admin):
        empty_data = {}
        response = admin_client.post('/api/users/', data=empty_data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/users/` с пустыми данными возвращаетe 400'
        )
        no_email_data = {
            'username': 'TestUser_noemail',
            'role': 'user'
        }
        response = admin_client.post('/api/users/', data=no_email_data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/users/` без email, возвращаетe статус 400'
        )
        valid_email = 'valid_email@foodgram.cook'
        no_username_data = {
            'email': valid_email,
            'role': 'user'
        }
        response = admin_client.post('/api/users/', data=no_username_data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/users/` без username, возвращаетe статус 400'
        )
        duplicate_email = {
            'username': 'TestUser_duplicate',
            'role': 'user',
            'email': admin.email
        }
        response = admin_client.post('/api/users/', data=duplicate_email)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/users/` с уже существующим email, возвращаете статус 400. '
            '`Email` должен быть уникальный у каждого прользователя'
        )
        duplicate_username = {
            'username': admin.username,
            'role': 'user',
            'email': valid_email
        }
        response = admin_client.post('/api/users/', data=duplicate_username)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/users/` с уже существующим email, возвращаете статус 400. '
            '`Email` должен быть уникальный у каждого прользователя'
        )
        data = {
            'username': admin.username,
            'role': 'user',
            'email': 'testuser@foodgram.cook'
        }
        response = admin_client.post('/api/users/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/users/` с неправильными данными возвращает статус 400. '
            '`Username` должен быть уникальный у каждого прользователя'
        )
        valid_data = {
            'username': 'TestUser_2',
            'role': 'user',
            'email': 'testuser2@foodgram.cook'
        }
        response = admin_client.post('/api/users/', data=valid_data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/users/` с правильными данными возвращает 201.'
        )
        valid_data = {
            'username': 'TestUser_3',
            'email': 'testuser3@foodgram.cook'
        }
        response = admin_client.post('/api/users/', data=valid_data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/users/`, при создании пользователя без указания роли, '
            'по умолчанию выдается роль user и возвращается статус 201.'
        )
        assert response.json().get('role') == 'user', (
            'Проверьте, что при POST запросе `/api/users/`, при создании пользователя без указания роли, '
            'по умолчанию выдается роль user и возвращается статус 201.'
        )
        data = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'test_username',
            'role': 'moderator',
            'email': 'testmoder2@foodgram.cook'
        }
        response = admin_client.post('/api/users/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/users/` с правильными данными возвращает 201.'
        )
        response_data = response.json()
        assert response_data.get('first_name') == data['first_name'], (
            'Проверьте, что при POST запросе `/api/users/` с правильными данными возвращаете `first_name`.'
        )
        assert response_data.get('last_name') == data['last_name'], (
            'Проверьте, что при POST запросе `/api/users/` с правильными данными возвращаете `last_name`.'
        )
        assert response_data.get('username') == data['username'], (
            'Проверьте, что при POST запросе `/api/users/` с правильными данными возвращаете `username`.'
        )
        assert response_data.get('role') == data['role'], (
            'Проверьте, что при POST запросе `/api/users/` с правильными данными возвращаете `role`.'
        )
        assert response_data.get('email') == data['email'], (
            'Проверьте, что при POST запросе `/api/users/` с правильными данными возвращаете `email`.'
        )
        User = get_user_model()
        users = User.objects.all()
        assert get_user_model().objects.count() == users.count(), (
            'Проверьте, что при POST запросе `/api/users/` вы создаёте пользователей.'
        )
        response = admin_client.get('/api/users/')
        data = response.json()
        assert len(data['results']) == users.count(), (
            'Проверьте, что при GET запросе `/api/users/` возвращаете данные с пагинацией. '
            'Значение параметра `results` не правильное'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_post_user_superuser(self, user_superuser_client):
        users = get_user_model().objects.all()
        users_before = users.count()
        valid_data = {
            'username': 'TestUser_3',
            'role': 'user',
            'email': 'testuser3@foodgram.cook'
        }
        response = user_superuser_client.post('/api/users/', data=valid_data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/users/` от суперпользователя, '
            'с правильными данными, возвращаете статус 201.'
        )
        users_after = users.count()
        assert users_after == users_before + 1, (
            'Проверьте, что при POST запросе `/api/users/` от суперпользователя, '
            'с правильными данными, создается пользователь.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_username_get_admin(self, admin_client, admin):
        user, moderator = create_users_api(admin_client)
        response = admin_client.get(f'/api/users/{admin.username}/')
        assert response.status_code != 404, (
            'Страница `/api/users/{username}/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/users/{username}/` с токеном админа возвращается статус 200'
        )
        response_data = response.json()
        assert response_data.get('username') == admin.username, (
            'Проверьте, что при GET запросе `/api/users/{username}/` возвращаете `username`.'
        )
        assert response_data.get('email') == admin.email, (
            'Проверьте, что при GET запросе `/api/users/{username}/` возвращаете `email`.'
        )

        response = admin_client.get(f'/api/users/{moderator.username}/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/users/{username}/` с токеном авторизации возвращается статус 200'
        )
        response_data = response.json()
        assert response_data.get('username') == moderator.username, (
            'Проверьте, что при GET запросе `/api/users/{username}/` возвращаете `username`.'
        )
        assert response_data.get('email') == moderator.email, (
            'Проверьте, что при GET запросе `/api/users/{username}/` возвращаете `email`.'
        )
        assert response_data.get('first_name') == moderator.first_name, (
            'Проверьте, что при GET запросе `/api/users/` возвращаете `first_name`.'
        )
        assert response_data.get('last_name') == moderator.last_name, (
            'Проверьте, что при GET запросе `/api/users/` возвращаете `last_name`.'
        )
        assert response_data.get('role') == moderator.role, (
            'Проверьте, что при GET запросе `/api/users/` возвращаете `role`.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_username_get_not_admin(self, moderator_client, admin):
        response = moderator_client.get(f'/api/users/{admin.username}/')
        assert response.status_code != 404, (
            'Страница `/api/users/{username}/` не найдена, проверьте этот адрес в *urls.py*'
        )
        code = 403
        assert response.status_code == code, (
            'Проверьте, что при GET запросе `/api/users/{username}/`'
            f' с токеном админа возвращается статус {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_username_patch_admin(self, admin_client, admin):
        user, moderator = create_users_api(admin_client)
        data = {
            'first_name': 'Admin',
            'last_name': 'Test',
        }
        response = admin_client.patch(f'/api/users/{admin.username}/', data=data)
        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/api/users/{username}/` '
            'с токеном авторизации возвращается статус 200'
        )
        test_admin = get_user_model().objects.get(username=admin.username)
        assert test_admin.first_name == data['first_name'], (
            'Проверьте, что при PATCH запросе `/api/users/{username}/` изменяете данные.'
        )
        assert test_admin.last_name == data['last_name'], (
            'Проверьте, что при PATCH запросе `/api/users/{username}/` изменяете данные.'
        )
        response = admin_client.patch(f'/api/users/{user.username}/', data={'role': 'admin'})
        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/api/users/{username}/` '
            'от пользователя с ролью admin можно изменить роль пользователя'
        )
        response = admin_client.patch(f'/api/users/{user.username}/', data={'role': 'owner'})
        assert response.status_code == 400, (
            'Проверьте, что при PATCH запросе `/api/users/{username}/` '
            'от пользователя с ролью admin нельзя назначать произвольные роли пользователя'
            'и возвращается статус 400'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_username_patch_moderator(self, moderator_client, user):
        data = {
            'first_name': 'New USer Firstname',
            'last_name': 'New USer Lastname',
        }
        response = moderator_client.patch(f'/api/users/{user.username}/', data=data)
        assert response.status_code == 403, (
            'Проверьте, что при PATCH запросе `/api/users/{username}/` '
            'пользователь с ролью moderator не может изменять данные других пользователей'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_username_patch_user(self, user_client, user):
        data = {
            'first_name': 'New USer Firstname',
            'last_name': 'New USer Lastname',
        }
        response = user_client.patch(f'/api/users/{user.username}/', data=data)
        assert response.status_code == 403, (
            'Проверьте, что при PATCH запросе `/api/users/{username}/` '
            'пользователь с ролью user не может изменять данные других пользователей'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_username_put_user_restricted(self, user_client, user):
        data = {
            'first_name': 'New USer Firstname',
            'last_name': 'New USer Lastname',
        }
        response = user_client.put(f'/api/users/{user.username}/', data=data)
        code = 403
        assert response.status_code == code, (
            'Проверьте, что PUT запрос на `/api/users/{username}/` '
            f'не доступен и возвращается статус {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_08_01_users_username_delete_admin(self, admin_client):
        user, moderator = create_users_api(admin_client)
        response = admin_client.delete(f'/api/users/{user.username}/')
        assert response.status_code == 204, (
            'Проверьте, что при DELETE запросе `/api/users/{username}/` возвращаете статус 204'
        )
        assert get_user_model().objects.count() == 2, (
            'Проверьте, что при DELETE запросе `/api/users/{username}/` удаляете пользователя'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_username_delete_moderator(self, moderator_client, user):
        users_before = get_user_model().objects.count()
        response = moderator_client.delete(f'/api/users/{user.username}/')
        assert response.status_code == 403, (
            'Проверьте, что при DELETE запросе `/api/users/{username}/`'
            'не от админа, возвращаете статус 403'
        )
        assert get_user_model().objects.count() == users_before, (
            'Проверьте, что при DELETE запросе `/api/users/{username}/`'
            'не от админа, не удаляете пользователя'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_username_delete_user(self, user_client, user):
        users_before = get_user_model().objects.count()
        response = user_client.delete(f'/api/users/{user.username}/')
        assert response.status_code == 403, (
            'Проверьте, что при DELETE запросе `/api/users/{username}/` '
            'не от админа, возвращаете статус 403'
        )
        assert get_user_model().objects.count() == users_before, (
            'Проверьте, что при DELETE запросе `/api/users/{username}/` '
            'не от админа, не удаляете пользователя'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_username_delete_superuser(self, user_superuser_client, user):
        users_before = get_user_model().objects.count()
        response = user_superuser_client.delete(f'/api/users/{user.username}/')
        code = 204
        assert response.status_code == code, (
            'Проверьте, что при DELETE запросе `/api/users/{username}/` '
            f'от суперпользователя, возвращаете статус {code}'
        )
        assert get_user_model().objects.count() == users_before - 1, (
            'Проверьте, что при DELETE запросе `/api/users/{username}/` '
            'от суперпользователя, пользователь удаляется.'
        )

    def check_permissions(self, user, user_name, admin):
        client_user = auth_client(user)
        response = client_user.get('/api/users/')
        assert response.status_code == 403, (
            f'Проверьте, что при GET запросе `/api/users/` '
            f'с токеном авторизации {user_name} возвращается статус 403'
        )
        data = {
            'username': 'TestUser9876',
            'role': 'user',
            'email': 'testuser9876@foodgram.cook'
        }
        response = client_user.post('/api/users/', data=data)
        assert response.status_code == 403, (
            f'Проверьте, что при POST запросе `/api/users/` '
            f'с токеном авторизации {user_name} возвращается статус 403'
        )

        response = client_user.get(f'/api/users/{admin.username}/')
        assert response.status_code == 403, (
            f'Проверьте, что при GET запросе `/api/users/{{username}}/` '
            f'с токеном авторизации {user_name} возвращается статус 403'
        )
        data = {
            'first_name': 'Admin',
            'last_name': 'Test'
        }
        response = client_user.patch(f'/api/users/{admin.username}/', data=data)
        assert response.status_code == 403, (
            f'Проверьте, что при PATCH запросе `/api/users/{{username}}/` '
            f'с токеном авторизации {user_name} возвращается статус 403'
        )
        response = client_user.delete(f'/api/users/{admin.username}/')
        assert response.status_code == 403, (
            f'Проверьте, что при DELETE запросе `/api/users/{{username}}/` '
            f'с токеном авторизации {user_name} возвращается статус 403'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_check_permissions(self, admin_client, admin):
        user, moderator = create_users_api(admin_client)
        self.check_permissions(user, 'обычного пользователя', admin)
        self.check_permissions(moderator, 'модератора', admin)

    @pytest.mark.django_db(transaction=True)
    def test_users_me_get_admin(self, admin_client, admin):
        user, moderator = create_users_api(admin_client)
        response = admin_client.get('/api/users/me/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/users/me/` от админа, возвращается статус 200'
        )
        response_data = response.json()
        assert response_data.get('username') == admin.username, (
            'Проверьте, что при GET запросе `/api/users/me/` возвращаете данные пользователя'
        )
        client_user = auth_client(moderator)
        response = client_user.get('/api/users/me/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/users/me/` с токеном авторизации возвращается статус 200'
        )
        response_data = response.json()
        assert response_data.get('username') == moderator.username, (
            'Проверьте, что при GET запросе `/api/users/me/` возвращаете данные пользователя'
        )
        assert response_data.get('role') == 'moderator', (
            'Проверьте, что при GET запросе `/api/users/me/` возвращаете данные пользователя'
        )
        assert response_data.get('email') == moderator.email, (
            'Проверьте, что при GET запросе `/api/users/me/` возвращаете данные пользователя'
        )
        response = client_user.delete('/api/users/me/')
        assert response.status_code == 405, (
            'Проверьте, что при DELETE запросе `/api/users/me/` возвращается статус 405'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_me_patch_admin(self, admin_client):
        user, moderator = create_users_api(admin_client)
        data = {
            'first_name': 'Admin',
            'last_name': 'Test'
        }
        response = admin_client.patch('/api/users/me/', data=data)
        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/api/users/me/` с токеном авторизации возвращается статус 200'
        )
        client_user = auth_client(moderator)
        response = client_user.patch('/api/users/me/', data={'first_name': 'NewTest'})
        test_moderator = get_user_model().objects.get(username=moderator.username)
        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/api/users/me/` с токеном авторизации возвращается статус 200'
        )
        assert test_moderator.first_name == 'NewTest', (
            'Проверьте, что при PATCH запросе `/api/users/me/` изменяете данные'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_me_patch_user(self, user_client):
        data = {
            'first_name': 'New user first name',
            'last_name': 'New user last name'
        }
        response = user_client.patch('/api/users/me/', data=data)
        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/api/users/me/`, '
            'пользователь с ролью user может изменить свои данные, и возвращается статус 200'
        )

        data = {
            'role': 'admin'
        }
        response = user_client.patch('/api/users/me/', data=data)
        response_json = response.json()
        assert response_json.get('role') == 'user', (
            'Проверьте, что при PATCH запросе `/api/users/me/`, '
            'пользователь с ролью user не может сменить себе роль'
        )
