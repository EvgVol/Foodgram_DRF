import pytest

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


# @pytest.fixture
# def auth_client_1(user_1):
#     token = Token.objects.get(user_1)
#     client = APIClient()
#     client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


# @pytest.fixture
# def auth_client_2(user_2):
#     token = Token.objects.get(user_2)
#     client = APIClient()
#     client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


# @pytest.fixture
# def auth_client_3(user_3):
#     token = Token.objects.get(user_3)
#     client = APIClient()
#     client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


@pytest.fixture
def unauth_client(
        db, tag_breakfast, tag_dinner, tag_supper, ingredient_1, ingredient_2,
        ingredient_3, user_1, user_2, user_3
):
    client = APIClient()
    return client


@pytest.fixture
def auth_client_1(unauth_client, user_1):
    unauth_client.force_authenticate(user=user_1)
    return unauth_client


@pytest.fixture
def auth_client_2(unauth_client, user_2):
    unauth_client.force_authenticate(user=user_2)
    return unauth_client


@pytest.fixture
def auth_client_3(unauth_client, user_3):
    unauth_client.force_authenticate(user=user_3)
    return unauth_client


@pytest.fixture
def auth_client_super(unauth_client, superuser):
    unauth_client.force_authenticate(user=superuser)
    return unauth_client


@pytest.fixture
def invalid_token_client(unauth_client):
    unauth_client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalid_token')
    return unauth_client