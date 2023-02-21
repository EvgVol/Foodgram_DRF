from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


def create_users_api(admin_client):
    data = {
        'username': 'TestUser',
        'role': 'user',
        'email': 'testuser@foodgram.cook'
    }
    admin_client.post('/api/users/', data=data)
    user = get_user_model().objects.get(username=data['username'])
    data = {
        'first_name': 'ModerFirstName',
        'last_name': 'ModerLastName',
        'username': 'TestModer',
        'role': 'moderator',
        'email': 'testmoder@foodgram.cook'
    }
    admin_client.post('/api/users/', data=data)
    moderator = get_user_model().objects.get(username=data['username'])
    return user, moderator


def auth_client(user):
    refresh = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {refresh.access_token}')
    return client