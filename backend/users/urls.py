from django.urls import include, path
from rest_framework import routers

from .views import UsersViewSet

app_name = 'users'


router = routers.DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('', incluse(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/me/', UserView.as_view(), name='me'),
]