from django.urls import include, path
from rest_framework import routers

from .views import CustomUserViewSet, set_password


router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('users/set_password/', set_password, name='set_password'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
