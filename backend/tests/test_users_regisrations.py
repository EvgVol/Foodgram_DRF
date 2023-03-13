import pytest
from django.contrib.auth import get_user_model
from django.core import mail


User = get_user_model()


class TestUserRegistration:
    url_signup = '/api/users/'
    url_token = '/api/auth/token/login/'
    url_admin_create_user = '/api/users/'

    @pytest.mark.django_db(transaction=True)
    def test_nodata_signup(self, client):
        request_type = 'POST'
        response = client.post(self.url_signup)

        assert response.status_code != 404, (
            f'Страница `{self.url_signup}` не найдена, проверьте этот адрес в *urls.py*'
        )
        code = 400
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{self.url_signup}` без параметров '
            f'не создается пользователь и возвращается статус {code}'
        )
        response_json = response.json()
        empty_fields = ['email', 'username']
        for field in empty_fields:
            assert (field in response_json.keys()
                    and isinstance(response_json[field], list)), (
                f'Проверьте, что при {request_type} запросе `{self.url_signup}` без параметров '
                f'в ответе есть сообщение о том, какие поля заполенены неправильно'
            )