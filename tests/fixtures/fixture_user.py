import pytest


@pytest.fixture
def superuser(django_user_model):
    return django_user_model.objects.create_superuser(
        username='TestSuperuser',
        email='testsuperuser@foodgram.cook',
        password='1234567',
        first_name='Admin',
        last_name='SuperUser'
    )


@pytest.fixture
def user_1(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser1',
        password='TestPassword1',
        email='test1@foodgram.cook',
        first_name='TestUser1',
        last_name='TestUser1'
    )


@pytest.fixture
def user_2(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser2',
        password='TestPassword2',
        email='test2@foodgram.cook',
        first_name='TestUser2',
        last_name='TestUser2'
    )


@pytest.fixture
def user_3(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser3',
        password='TestPassword3',
        email='test3@foodgram.cook',
        first_name='TestUser3',
        last_name='TestUser3'
    )


@pytest.fixture
def superuser(django_user_model):
    return django_user_model.objects.create_superuser(
        username='admin',
        password='TestPassword4',
        email='admin@foodgram.cook',
        first_name='TestAdmin-fn',
        last_name='TestAdmin_ln'
    )
