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

    @pytest.mark.django_db(transaction=True)
    def test_02_follow_post_guest_users(self, client, user_2):
        response = client.post(f'/api/users/{user_2.id}/subscribe/')
        assert response.status_code != 404, (
            'Страница `/api/users/subscriptions/` не найдена, проверьте'
            'этот адрес в *urls.py*'
        )
        assert response.status_code == 401, (
            'Проверьте, что при POST запросе от анонимного пользователя'
            ' страница `/api/users/{id}/subscribe/` возвращает статус 401'
        )

    @pytest.mark.django_db(transaction=True)
    def test_02_01_follow_post_auth_users(
        self, auth_client_1, user_1, user_2
    ):
        response = auth_client_1.post(f'/api/users/{user_2.id}/subscribe/')
        assert response.status_code != 404, (
            'Страница `/api/users/subscriptions/` не найдена, проверьте'
            'этот адрес в *urls.py*'
        )
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе от авторизованного пользователя'
            ' страница `/api/users/{id}/subscribe/` возвращает статус 201'
        )
        response = auth_client_1.get('/api/users/subscriptions/')
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
        assert data['count'] == 1, (
            'Проверьте, что при GET запросе `/api/users/subscriptions/` '
            'возвращаете данные с пагинацией. Значение параметра `count` '
            'не правильное'
        )
        assert type(data['results']) == list, (
            'Проверьте, что при GET запросе `/api/users/subscriptions/` '
            'возвращаете данные пагинацией. Тип параметра `results` должен '
            'быть список'
        )
        assert type(data['results'][0].get('recipes')) == list, (
            'Проверьте, что при GET запросе `/api/users/subscriptions/` '
            'возвращаете данные пагинацией. Тип параметра `recipes` должен '
            'быть список'
        )
        assert (
            len(data['results']) == 1
            and data['results'][0].get('username') == user_2.username
            and data['results'][0].get('email') == user_2.email
        ), (
            'Проверьте, что при GET запросе `/api/users/subscriptions/` '
            'возвращаете данные с пагинацией. Значение параметра `results` '
            'не правильное'
        )
        user_2_as_dict = {
            'id': user_2.id,
            'username': user_2.username,
            'email': user_2.email,
            'first_name': user_2.first_name,
            'last_name': user_2.last_name,
            'is_subscribed': True,
            'recipes': [],   ###################### <<<<<<<<<<<< это заглушка. исправить в дальнейшем
            'recipes_count': 0, ###################### <<<<<<<<<<<< это заглушка. исправить в дальнейшем
        }
        assert data['results'] == [user_2_as_dict], (
            'Проверьте, что при GET запросе `/api/users/subscriptions/` '
            'возвращается искомый пользователь со всеми необходимыми полями, '
            'включая `is_subscribed`, `recipes`, `recipes_count` '
        )
        response = auth_client_1.post(f'/api/users/{user_2.id}/subscribe/')
        assert response.status_code == 400, (
            'Проверьте, что при наличии подписки'
            ' страница `/api/users/{id}/subscribe/` возвращает статус 400'
        )
        response = auth_client_1.delete(f'/api/users/{user_2.id}/subscribe/')
        assert response.status_code == 204, (
            'Проверьте, что при DELETE запросе и при наличии подписки'
            ' страница `/api/users/{id}/subscribe/` возвращает статус 204'
        )
        response = auth_client_1.post(f'/api/users/{user_1.id}/subscribe/')
        assert response.status_code == 400, (
            'Проверьте, что при авторизованный пользователь не может'
            'подписаться на самого себя и страница '
            '`/api/users/{id}/subscribe/` возвращает статус 400'
        )

    @pytest.mark.django_db(transaction=True)
    def test_03_follow_del_guest_users(self, client, user_2):
        response = client.delete(f'/api/users/{user_2.id}/subscribe/')
        assert response.status_code != 404, (
            'Страница `/api/users/subscriptions/` не найдена, проверьте'
            'этот адрес в *urls.py*'
        )
        assert response.status_code == 401, (
            'Проверьте, что при DELETE запросе от анонимного пользователя'
            ' страница `/api/users/{id}/subscribe/` возвращает статус 401'
        )

    @pytest.mark.django_db(transaction=True)
    def test_04_follow_del_auth_users(self, auth_client_1, user_2):
        response = auth_client_1.delete(f'/api/users/{user_2.id}/subscribe/')
        assert response.status_code == 404 or 400, (
            'Проверьте, что при DELETE запросе от авторизованного '
            'пользователя страница `/api/users/{id}/subscribe/` '
            'возвращает статус: `Объект не найден` или `Ошибка подписки`'
        )
