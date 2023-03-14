import pytest
from django.contrib.auth import get_user_model

class Test01UserAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_users_not_authenticated(self, unauth_client):
        response = unauth_client.get('/api/users/')

        assert response.status_code != 404, (
            'Страница `/api/users/` не найдена, проверьте этот адрес в *urls.py*'
        )

        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/users/` без токена авторизации возвращается статус 401'
        )

    @pytest.mark.django_db(transaction=True)
    def test_02_users_id_not_authenticated(self, unauth_client, user_1):
        response = unauth_client.get(f'/api/users/{user_1.id}/')

        assert response.status_code != 404, (
            'Страница `/api/users/{id}/` не найдена, проверьте этот адрес в *urls.py*'
        )

        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/users/{id}/` без токена авторизации возвращается статус 401'
        )

    @pytest.mark.django_db(transaction=True)
    def test_03_users_me_not_authenticated(self, unauth_client):
        response = unauth_client.get('/api/users/me/')

        assert response.status_code != 404, (
            'Страница `/api/users/me/` не найдена, проверьте этот адрес в *urls.py*'
        )

        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/users/me/` без токена авторизации возвращается статус 401'
        )

    @pytest.mark.django_db(transaction=True)
    def test_04_users_get_admin(self, auth_client_1, user_1):
        response = auth_client_1.get('/api/users/')
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
            and data['results'][0].get('username') == user_1.username
            and data['results'][0].get('email') == user_1.email
        ), (
            'Проверьте, что при GET запросе `/api/users/` возвращаете данные с пагинацией. '
            'Значение параметра `results` не правильное'
        )

    @pytest.mark.django_db(transaction=True)
    def test_04_02_users_get_search(self, auth_client_1, user_1):
        url = '/api/users/'
        search_url = f'{url}?search={user_1.id}'
        response = auth_client_1.get(search_url)
        assert response.status_code != 404, (
            'Страница `/api/users/?search={id}` не найдена, проверьте этот адрес в *urls.py*'
        )
        reponse_json = response.json()
        assert 'results' in reponse_json and isinstance(reponse_json.get('results'), list), (
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
            'возвращается искомый пользователь со всеми необходимыми полями, включая `is_subscribed`'
        )