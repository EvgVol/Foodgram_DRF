from http import HTTPStatus

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from recipes.models import Tag, Ingredient, Recipe, Favorite, ShoppingCart, IngredientInRecipe
from users.models import User, Follow


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            email='author@foodgram.cook',
            username='author',
            first_name='author_first_name',
            last_name='author_last_name',
            password='testPass1'
        )
        cls.not_an_author = User.objects.create_user(
            email='no_author@foodgram.cook',
            username='no_author',
            first_name='no_author_first_name',
            last_name='no_author_last_name',
            password='testPass1'
        )
        cls.tag = Tag.objects.create(
            name='easy',
            color='#FF0000',
            slug='easy'
        )
        cls.ingredient = Ingredient.objects.create(
            name='Молоко',
            measurement_unit='г',
        )
        
        cls.follow = Follow.objects.create(
            user=cls.not_an_author,
            author=cls.user
        )
        cls.templates_avalible_guest = {
            'user_id': f'/api/users/{cls.user.id}/',
            'recipes': '/api/recipes/',
            'recipe_id': f'/api/recipes/{cls.recipe.id}',
        }
        cls.templates_notavalible_guest = {
            'users': '/api/users/',
            'users_subscribe': f'/api/users/{cls.user.id}/subscribe/',
            'users_subscriptions': '/api/users/subscriptions/',
            'users_me': '/api/users/me/',
            'tags': '/api/tags/',
            'tags_id': f'api/tags/{cls.tag.id}/',
            'recipe_favorite': f'/api/recipes/{cls.recipe.id}/favorite/'
        }
        
    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.not_author = Client()
        self.not_author.force_login(self.not_an_author)
    
    def test_unexisting_page(self):
        """Провека несуществующей страницы."""
        response = self.authorized_client.get('/unexisting/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_recipes_url_exists_at_desired_location(self):
        """Проверка доступности адреса /api/recipe/."""
        response = self.authorized_client.get('/api/recipes/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_tags_url_exists_at_desired_location(self):
        """Проверка доступности адреса /api/tags/."""
        response = self.authorized_client.get('/api/tags/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_users_list_url_unavailable_anonymous(self):
        """Страница /api/users/ недоступна неавторизованному пользователю."""
        response = self.guest_client.get('/api/users/')
        self.assertEqual(response.status_code, 401)
