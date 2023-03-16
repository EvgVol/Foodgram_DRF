import pytest
from django.contrib.auth import get_user_model


class Test03UserAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_users_not_authenticated(self, unauth_client):
        response = unauth_client.get('/api/users/')

        assert response.status_code != 404, (
            'Страница `/api/users/` не найдена, проверьте этот адрес в '
            '*urls.py*'
        )

        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/users/` без токена '
            'авторизации возвращается статус 401'
        )

    @pytest.mark.django_db(transaction=True)
    def test_02_users_id_not_authenticated(self, unauth_client, user_1):
        response = unauth_client.get(f'/api/users/{user_1.id}/')

        assert response.status_code != 404, (
            'Страница `/api/users/{id}/` не найдена, проверьте этот адрес в '
            '*urls.py*'
        )

        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/users/{id}/` без токена '
            'авторизации возвращается статус 401'
        )

    @pytest.mark.django_db(transaction=True)
    def test_03_users_me_not_authenticated(self, unauth_client):
        response = unauth_client.get('/api/users/me/')

        assert response.status_code != 404, (
            'Страница `/api/users/me/` не найдена, проверьте этот адрес в '
            '*urls.py*'
        )

        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/users/me/` без токена '
            'авторизации возвращается статус 401'
        )

    @pytest.mark.django_db(transaction=True)
    def test_04_users_get_users(self, auth_client_1, user_1):
        response = auth_client_1.get('/api/users/')
        assert response.status_code != 404, (
            'Страница `/api/users/` не найдена, проверьте этот адрес в '
            '*urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/users/` с токеном '
            'авторизации возвращается статус 200'
        )
        data = response.json()
        assert 'count' in data, (
            'Проверьте, что при GET запросе `/api/users/` возвращаете данные '
            'с пагинацией. Не найден параметр `count`'
        )
        assert 'next' in data, (
            'Проверьте, что при GET запросе `/api/users/` возвращаете данные '
            'с пагинацией. '
            'Не найден параметр `next`'
        )
        assert 'previous' in data, (
            'Проверьте, что при GET запросе `/api/users/` возвращаете данные '
            'с пагинацией. '
            'Не найден параметр `previous`'
        )
        assert 'results' in data, (
            'Проверьте, что при GET запросе `/api/users/` возвращаете данные '
            'с пагинацией. '
            'Не найден параметр `results`'
        )
        assert data['count'] == 1, (
            'Проверьте, что при GET запросе `/api/users/` возвращаете данные '
            'с пагинацией. '
            'Значение параметра `count` не правильное'
        )
        assert type(data['results']) == list, (
            'Проверьте, что при GET запросе `/api/users/` возвращаете данные '
            'с пагинацией. '
            'Тип параметра `results` должен быть список'
        )
        assert (
            len(data['results']) == 1
            and data['results'][0].get('username') == user_1.username
            and data['results'][0].get('email') == user_1.email
        ), (
            'Проверьте, что при GET запросе `/api/users/` возвращаете данные '
            'с пагинацией. '
            'Значение параметра `results` не правильное'
        )
        user_1_as_dict = {
            'id': user_1.id,
            'username': user_1.username,
            'email': user_1.email,
            'first_name': user_1.first_name,
            'last_name': user_1.last_name,
            'is_subscribed': False,
        }
        assert response.json()['results'] == [user_1_as_dict], (
            'Проверьте, что при GET запросе `/api/users/me/` '
            'возвращается искомый пользователь со всеми необходимыми полями, '
            'включая `is_subscribed`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_04_02_users_get_search(self, auth_client_1, user_1):
        url = '/api/users/'
        search_url = f'{url}?search={user_1.id}'
        response = auth_client_1.get(search_url)
        assert response.status_code != 404, (
            'Страница `/api/users/?search={id}` не найдена, проверьте этот '
            'адрес в *urls.py*'
        )
        reponse_json = response.json()
        assert 'results' in reponse_json and isinstance(
            reponse_json.get('results'), list
        ), (
            'Проверьте, что при GET запросе `/api/users/?search={id}` '
            'результаты возвращаются под ключом `results` и в виде списка.'
        )
        users_count = get_user_model().objects.filter(id=user_1.id).count()
        assert len(reponse_json['results']) == users_count, (
            'Проверьте, что при GET запросе `/api/users/?search={id}` '
            'возвращается только пользователь с указанным в поиске id'
        )
        user_1_as_dict = {
            'id': user_1.id,
            'username': user_1.username,
            'email': user_1.email,
            'first_name': user_1.first_name,
            'last_name': user_1.last_name,
            'is_subscribed': False,
        }
        assert reponse_json['results'] == [user_1_as_dict], (
            'Проверьте, что при GET запросе `/api/users/?search={id}` '
            'возвращается искомый пользователь со всеми необходимыми полями, '
            'включая `is_subscribed`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_04_01_users_get_admin_only(self, auth_client_super):
        response = auth_client_super.get('/api/users/')
        assert response.status_code != 404, (
            'Страница `/api/users/` не найдена, проверьте этот адрес в '
            '*urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/users/` от '
            'суперпользователя с токеном авторизации возвращается статус 200'
        )
        data = response.json()
        assert 'count' in data, (
            'Проверьте, что при GET запросе `/api/users/` от '
            'суперпользователя возвращаете данные с пагинацией. '
            'Не найден параметр `count`'
        )
        assert 'next' in data, (
            'Проверьте, что при GET запросе `/api/users/` от '
            'суперпользователя возвращаете данные с пагинацией. '
            'Не найден параметр `next`'
        )
        assert 'previous' in data, (
            'Проверьте, что при GET запросе `/api/users/` от '
            'суперпользователя возвращаете данные с пагинацией. '
            'Не найден параметр `previous`'
        )
        assert 'results' in data, (
            'Проверьте, что при GET запросе `/api/users/` от '
            'суперпользователя возвращаете данные с пагинацией. '
            'Не найден параметр `results`'
        )
        assert data['count'] == 4, (
            'Проверьте, что при GET запросе `/api/users/` от '
            'суперпользователя возвращаете данные с пагинацией. '
            'Значение параметра `count` не правильное'
        )
        assert type(data['results']) == list, (
            'Проверьте, что при GET запросе `/api/users/` от '
            'суперпользователя возвращаете данные с пагинацией. '
            'Тип параметра `results` должен быть список'
        )
        assert (
            len(data['results']) == 4
        ), (
            'Проверьте, что при GET запросе `/api/users/` от '
            'суперпользователя возвращаете данные с пагинацией. '
            'Значение параметра `results` не правильное'
        )

    @pytest.mark.django_db(transaction=True)
    def test_05_01_users_post_guest(
        self, client, auth_client_super, superuser
    ):
        empty_data = {}
        response = client.post('/api/users/', data=empty_data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/users/` с пустыми данными '
            'возвращаетe 400'
        )
        no_email_data = {
            'username': 'TestUser_noemail',
            'password': 'testPass1'
        }
        response = client.post('/api/users/', data=no_email_data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/users/` без email, '
            'возвращаетe статус 400'
        )
        valid_email = 'valid_email@foodgram.cook'
        no_username_data = {
            'email': valid_email,
            'password': 'testPass1'
        }
        response = client.post('/api/users/', data=no_username_data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/users/` без username, '
            'возвращаетe статус 400'
        )
        duplicate_email = {
            'username': 'TestSuperUser_duplicate',
            'email': superuser.email
        }
        response = client.post('/api/users/', data=duplicate_email)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/users/` с уже существующим'
            'email, возвращаете статус 400. '
            '`Email` должен быть уникальный у каждого прользователя'
        )
        duplicate_username = {
            'username': superuser.username,
            'email': valid_email
        }
        response = client.post('/api/users/', data=duplicate_username)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/users/` с уже существующим'
            'username, возвращаете статус 400. '
            '`Username` должен быть уникальный у каждого прользователя'
        )
        unvalid_data_username = {
            'username': (
                'loooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooong '
            ),
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'password': 'qwerty1123zxc',
            'email': 'new_NEW_user@foodgram.cook'
        }
        response = client.post('/api/users/', data=unvalid_data_username)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/users/` установлена '
            'максимальная длина `username`'
        )
        unvalid_data_username_me = {
            'username': 'me',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'password': 'qwerty1123zxc',
            'email': 'new_NEW_user@foodgram.cook'
        }
        response = client.post('/api/users/', data=unvalid_data_username_me)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/users/` нельзя создать '
            'пользователем с `username` = me'
        )
        unvalid_data_first_name = {
            'username': 'Username',
            'first_name': (
                'loooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooong '
            ),
            'last_name': 'Last',
            'password': 'qwerty1123zxc',
            'email': 'new_NEW_user@foodgram.cook'
        }
        response = client.post('/api/users/', data=unvalid_data_first_name)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/users/` установлена '
            'максимальная длина `first_name`'
        )
        unvalid_data_last_name = {
            'username': 'Username',
            'first_name': 'First',
            'last_name': (
                'loooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooong '
            ),
            'password': 'qwerty1123zxc',
            'email': 'new_NEW_user@foodgram.cook'
        }
        response = client.post('/api/users/', data=unvalid_data_last_name)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/users/` установлена '
            'максимальная длина `last_name`'
        )
        unvalid_data_email = {
            'username': 'Username',
            'first_name': 'First',
            'last_name': 'Last',
            'password': 'qwerty1123zxc',
            'email': (
                'loooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'oooooooooooooooooooooooooooooooooooooooooooooooooo@ooon.com '
            )
        }
        response = client.post('/api/users/', data=unvalid_data_email)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/users/` установлена '
            'максимальная длина `email`'
        )
        data = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'test_username',
            'password': 'qwerty1123zxc',
            'email': 'new_user@foodgram.cook'
        }
        response = client.post('/api/users/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/users/` с правильными '
            'данными возвращает 201.'
        )
        response_data = response.json()
        assert response_data.get('first_name') == data['first_name'], (
            'Проверьте, что при POST запросе `/api/users/` с правильными '
            'данными возвращаете `first_name`.'
        )
        assert response_data.get('last_name') == data['last_name'], (
            'Проверьте, что при POST запросе `/api/users/` с правильными '
            'данными возвращаете `last_name`.'
        )
        assert response_data.get('username') == data['username'], (
            'Проверьте, что при POST запросе `/api/users/` с правильными '
            'данными возвращаете `username`.'
        )
        assert response_data.get('email') == data['email'], (
            'Проверьте, что при POST запросе `/api/users/` с правильными '
            'данными возвращаете `email`.'
        )
        user = get_user_model()
        users = user.objects.all()
        assert get_user_model().objects.count() == users.count(), (
            'Проверьте, что при POST запросе `/api/users/` вы создаёте '
            'пользователей.'
        )
        response = auth_client_super.get('/api/users/')
        data = response.json()
        assert len(data['results']) == 5, (
            'Проверьте, что при GET запросе `/api/users/` возвращаете '
            'данные с пагинацией. '
            'Значение параметра `results` не правильное'
        )

    @pytest.mark.django_db(transaction=True)
    def test_05_02_users_post_user_superuser(self, auth_client_super):
        users = get_user_model().objects.all()
        users_before = users.count()
        valid_data = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'test_username',
            'password': 'qwerty1123zxc',
            'email': 'new_user@foodgram.cook'
        }
        response = auth_client_super.post('/api/users/', data=valid_data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/users/` от '
            'суперпользователя, с правильными данными, возвращаете '
            'статус 201.'
        )
        users_after = users.count()
        assert users_after == users_before + 1, (
            'Проверьте, что при POST запросе `/api/users/` от '
            'суперпользователя, с правильными данными, создается '
            'пользователь.'
        )
        unvalid_data_username = {
            'username': (
                'loooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooong '
            ),
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'password': 'qwerty1123zxc',
            'email': 'new_NEW_user@foodgram.cook'
        }
        response = auth_client_super.post(
            '/api/users/', data=unvalid_data_username
        )
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/users/` установлена '
            'максимальная длина `username`'
        )
        unvalid_data_first_name = {
            'username': 'Username',
            'first_name': (
                'loooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooong '
            ),
            'last_name': 'Last',
            'password': 'qwerty1123zxc',
            'email': 'new_NEW_user@foodgram.cook'
        }
        response = auth_client_super.post(
            '/api/users/', data=unvalid_data_first_name
        )
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/users/` установлена '
            'максимальная длина `first_name`'
        )
        unvalid_data_last_name = {
            'username': 'Username',
            'first_name': 'First',
            'last_name': (
                'loooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooong '
            ),
            'password': 'qwerty1123zxc',
            'email': 'new_NEW_user@foodgram.cook'
        }
        response = auth_client_super.post(
            '/api/users/', data=unvalid_data_last_name
        )
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/users/` установлена '
            'максимальная длина `last_name`'
        )
        unvalid_data_email = {
            'username': 'Username',
            'first_name': 'First',
            'last_name': 'Last',
            'password': 'qwerty1123zxc',
            'email': (
                'loooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo '
                'oooooooooooooooooooooooooooooooooooooooooooooooooo@ooon.com '
            )
        }
        response = auth_client_super.post(
            '/api/users/', data=unvalid_data_email
        )
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/users/` установлена '
            'максимальная длина `email`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_06_01_users_id_patch_admin(
        self, auth_client_super, auth_client_1, user_1
    ):
        data = {
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName',
        }
        response = auth_client_1.patch(f'/api/users/{user_1.id}/', data=data)
        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/api/users/{id}/` '
            'с токеном авторизации возвращается статус 200'
        )
        test_data = get_user_model().objects.get(id=user_1.id)
        assert test_data.first_name == data['first_name'], (
            'Проверьте, что при PATCH запросе `/api/users/{id}/` изменяете '
            'имя.'
        )
        assert test_data.last_name == data['last_name'], (
            'Проверьте, что при PATCH запросе `/api/users/{id}/` изменяете '
            'фамилию.'
        )
        response = auth_client_super.patch(
            f'/api/users/{user_1.id}/', data={'first_name': 'New2FirstName'}
        )
        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/api/users/{id}/` '
            'от суперпользователя можно изменить Имя пользователя'
        )
        response = auth_client_super.patch(
            f'/api/users/{user_1.id}/', data={'last_name': 'NewLastName'}
        )
        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/api/users/{id}/` '
            'от суперпользователя можно изменить Фамилию пользователя'
        )

    @pytest.mark.django_db(transaction=True)
    def test_06_02_users_id_patch_user(self, auth_client_1, user_2):
        data = {
            'first_name': 'New USer Firstname',
            'last_name': 'New USer Lastname'
        }
        response = auth_client_1.patch(f'/api/users/{user_2.id}/', data=data)
        assert response.status_code == 404, (
            'Проверьте, что при PATCH запросе `/api/users/{id}/` '
            'одним пользователем данные другого пользователя скрыты. '
        )

    @pytest.mark.django_db(transaction=True)
    def test_06_03_users_me_patch_user(self, auth_client_1):
        data = {
            'first_name': 'New user first name',
            'last_name': 'New user last name',
        }
        response = auth_client_1.patch('/api/users/me/', data=data)
        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/api/users/me/`, '
            'пользователь может изменить свои данные, и возвращается'
            ' статус 200'
        )

    @pytest.mark.django_db(transaction=True)
    def test_07_01_users_id_delete_users(self, auth_client_1, user_2):
        users_before = get_user_model().objects.count()
        response = auth_client_1.delete(f'/api/users/{user_2.id}/')
        assert response.status_code == 403, (
            'Проверьте, что при DELETE запросе `/api/users/{id}/` '
            'возвращаете статус 403'
        )
        assert get_user_model().objects.count() == users_before, (
            'Проверьте, что при DELETE запросе `/api/users/{id}/` '
            'не удаляете пользователя'
        )

    @pytest.mark.django_db(transaction=True)
    def test_07_02_users_id_delete_super(self, auth_client_super, user_1):
        users_before = get_user_model().objects.count()
        response = auth_client_super.delete(
            f'/api/users/{user_1.id}/',
            data={'current_password': 'TestPassword4'}
        )
        code = 204
        assert response.status_code == code, (
            'Проверьте, что при DELETE запросе `/api/users/{id}/` '
            f'от суперпользователя, возвращаете статус {code}'
        )
        assert get_user_model().objects.count() == users_before - 1, (
            'Проверьте, что при DELETE запросе `/api/users/{id}/` '
            'от суперпользователя, пользователь удаляется.'
        )
