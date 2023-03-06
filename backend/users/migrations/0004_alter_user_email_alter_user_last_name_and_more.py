# Generated by Django 4.1.7 on 2023-03-05 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_follow_options_alter_user_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(help_text='Набор символов не более 150', max_length=254, unique=True, verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(help_text='Набор символов не более 150', max_length=150, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(help_text='Набор символов не более 150', max_length=150, verbose_name='Пароль'),
        ),
    ]
