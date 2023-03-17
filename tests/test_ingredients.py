import pytest


class Test05IngredientAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_ingredient_avalible_guest_users(self, client, ingredient_1):
        response = client.get('/api/ingredients/')
        assert response.status_code != 404, (
            'Страница `/api/tags/` не найдена, проверьте этот адрес в '
            '*urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, cтраница `/api/ingredients/` должна быть доступна '
            'всем'
        )

        response = client.get(f'/api/ingredients/{ingredient_1.id}/')
        assert response.status_code == 200, (
            'Проверьте, cтраница `/api/ingredients/{id}/` должна быть '
            'доступна всем'
        )
        ingredient_as_dict = {
            'id': ingredient_1.id,
            'name': ingredient_1.name,
            'measurement_unit': ingredient_1.measurement_unit
        }
        assert response.json() == ingredient_as_dict, (
            'Проверьте, что при GET запросе `/api/ingredients/{id}/` '
            'возвращается ингредиент со всеми необходимыми полями'
        )
        assert response.status_code != 404, (
            'Проверьте, что при GET запросе `/api/ingredients/{id}/` '
            'возвращается статус 200'
        )


    @pytest.mark.django_db(transaction=True)
    def test_02_ingredients_prohibition_post_del_patch(
        self, client, auth_client_1, auth_client_super, ingredient_1,
    ):
        data = {
            'name': 'test',
            'measurement_unit': 'test'
        }
        response = client.post('/api/ingredients/', data=data)
        assert response.status_code != 201, (
            'Проверьте, что при POST запросе `/api/ingredients/{id}/` '
            'возвращается статус 405'
        )
        assert response.status_code == 405, (
            'Проверьте, что при POST запросе `/api/ingredients/` возвращается'
            ' статус 405'
        )
        response = auth_client_1.post('/api/ingredients/', data=data)
        assert response.status_code == 405, (
            'Проверьте, что при POST запросе `/api/ingredients/` возвращается'
            ' статус 405'
        )
        response = auth_client_super.post('/api/ingredients/', data=data)
        assert response.status_code == 405, (
            'Проверьте, что при POST запросе `/api/ingredients/` возвращается'
            'статус 405'
        )
        response = auth_client_super.delete(
            f'/api/ingredients/{ingredient_1.id}/'
        )
        assert response.status_code == 405, (
            'Проверьте, что при DELETE запросе `/api/ingredients/{id}/` '
            'возвращается статус 405'
        )
