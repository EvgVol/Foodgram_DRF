import pytest


@pytest.fixture
def user_1(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser1', password='TestPassword', email='test1@foodgram.cook',
        first_name='TestUser1', last_name='TestUser1'
    )


@pytest.fixture
def user_2(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser2', password='TestPassword', email='test2@foodgram.cook')


@pytest.fixture
def user_3(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser3', password='TestPassword', email='test3@foodgram.cook')
