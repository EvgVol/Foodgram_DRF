from pathlib import Path

from django.db.models.signals import post_delete
from django.dispatch import receiver
from rest_framework import response, status
from rest_framework.generics import get_object_or_404

from recipes.models import Recipe
from api.serializers import ShowRecipeAddedSerializer


def add_and_del(self, model, request, pk):
        """Опция добавления и удаления рецепта."""
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        obj = model.objects.filter(user=user, recipe__id=pk)

        if request.method == 'POST':
            if obj.exists():
                return response.Response(
                    {'warning': 'Второй раз нельзя добавить рецепт.'},
                    status=status.HTTP_400_BAD_REQUEST)
            serializer = ShowRecipeAddedSerializer(recipe)
            model.objects.create(user=user, recipe=recipe)
            return response.Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        if request.method == 'DELETE':
            if obj.exists():
                obj.delete()
                return response.Response(
                    {'message': 'Рецепт успешно удален'},
                    status=status.HTTP_204_NO_CONTENT)
            return response.Response(
                {'errors': 'Нельзя удалить то чего нет'},
                status=status.HTTP_400_BAD_REQUEST
            )


@receiver(post_delete, sender=Recipe)
def delete_image(sender, instance, *a, **kw):
    """Удаляет картинку при удаление рецепта."""
    image = Path(instance.image.path)
    if image.exists():
        image.unlink()
