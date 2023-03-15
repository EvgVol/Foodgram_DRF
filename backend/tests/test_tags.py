import pytest


class Test04TagAPI:

    @pytest.mark.django_db(transaction=True)
    def test_tags_avalible_users(self, client, tag_breakfast):
        response = client.get('/api/tags/')
        assert response.status_code != 404, (
            'Страница `/api/tags/` не найдена, проверьте этот адрес в '
            '*urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, cтраница `/api/tags/` должна быть доступна '
            'анонимным пользователям'
        )
        response = client.get(f'/api/tags/{tag_breakfast.id}')
        assert response.status_code == 301, (
            'Проверьте, cтраница `/api/tags/{id}` перенаправляет '
            'анонимного пользователя на другую страницу'
        )