import pytest
from recipes.models import Recipe


class Test07RecipeAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_recipe_get_users(
        self, client, auth_client_1, recipes
    ):
        response  = client.get(recipes)
        assert response.status_code == 200, (
            f'Проверьте, что при GET запросе страница `{recipes}` '
            'возвращает статус 200'
        )
        response  = auth_client_1.get(recipes)
        assert response.status_code == 200, (
            f'Проверьте, что при GET запросе страница `{recipes}` '
            'возвращает статус 200'
        )
        recipe_count = Recipe.objects.count()
        assert response.json().get('count') == recipe_count, (
            f'Проверьте, что при GET запросе страница `{recipes}` '
            'возвращается правильное количество рецептов'
        )
        data = response.json()
        assert 'count' in data, (
            f'Проверьте, что при GET запросе `{recipes}` возвращаете данные'
             ' с пагинацией. Не найден параметр `count`'
        )
        assert 'next' in data, (
            f'Проверьте, что при GET запросе `{recipes}` возвращаете данные'
             ' с пагинацией. Не найден параметр `next`'
        )
        assert 'previous' in data, (
            f'Проверьте, что при GET запросе `{recipes}` возвращаете данные'
             ' с пагинацией. Не найден параметр `previous`'
        )
        assert 'results' in data, (
            f'Проверьте, что при GET запросе `{recipes}` возвращаете данные'
             ' с пагинацией. Не найден параметр `results`'
        )
        assert type(data['results']) == list, (
            f'Проверьте, что при GET запросе `{recipes}` возвращаете данные'
             ' с пагинацией. Тип параметра `results` должен быть список'
        )
        assert (
            len(data['results']) == recipe_count
        ), (
            f'Проверьте, что при GET запросе `{recipes}` '
             'возвращаете данные с пагинацией. Значение параметра `results` '
             'не правильное'
        )
