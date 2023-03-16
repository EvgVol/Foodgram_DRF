import pytest


class Test06FollowingAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_follow_get_users(self, client, auth_client_1):
        response = client.get('/api/users/subscriptions/')
        assert response.status_code == 401, (
            'Проверьте, что при GET запросе от анонимного пользователя'
            ' страница `/api/users/subscriptions/` возвращает статус 401'
        )
        assert response.status_code != 404, (
            'Страница `/api/users/subscriptions/` не найдена, проверьте'
            'этот адрес в *urls.py*'
        )
        response = auth_client_1.get('/api/users/subscriptions/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе от авторизованного пользователя'
            ' страница `/api/users/subscriptions/` возвращает статус 200'
        )
        assert response.status_code != 404, (
            'Страница `/api/users/subscriptions/` не найдена, проверьте'
            'этот адрес в *urls.py*'
        )
        data = response.json()
        assert 'count' in data, (
            'Проверьте, что при GET запросе `/api/users/subscriptions/` '
            'возвращаете данные с пагинацией. Не найден параметр `count`'
        )
        assert 'next' in data, (
            'Проверьте, что при GET запросе `/api/users/subscriptions/` '
            'возвращаете данные с пагинацией. Не найден параметр `next`'
        )
        assert 'previous' in data, (
            'Проверьте, что при GET запросе `/api/users/subscriptions/` '
            'возвращаете данные с пагинацией. Не найден параметр `previous`'
        )
        assert 'results' in data, (
            'Проверьте, что при GET запросе `/api/users/subscriptions/` '
            'возвращаете данные с пагинацией. Не найден параметр `results`'
        )
        assert data['count'] == 0, (
            'Проверьте, что при GET запросе `/api/users/subscriptions/` '
            'возвращаете данные с пагинацией. Значение параметра `count` '
            'не правильное'
        )
        assert type(data['results']) == list, (
            'Проверьте, что при GET запросе `/api/users/subscriptions/` '
            'возвращаете данные пагинацией. Тип параметра `results` должен '
            'быть список'
        )

    @pytest.mark.django_db(transaction=True)
    def test_02_follow_post_users(self, client, auth_client_1, user_2):
        response = client.post(f'/api/users/{user_2.id}/subscribe/')
        assert response.status_code != 404, (
            'Страница `/api/users/subscriptions/` не найдена, проверьте'
            'этот адрес в *urls.py*'
        )
        assert response.status_code == 401, (
            'Проверьте, что при POST запросе от анонимного пользователя'
            ' страница `/api/users/{id}/subscribe/` возвращает статус 401'
        )
