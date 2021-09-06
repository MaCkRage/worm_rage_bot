from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    telegram_id = models.IntegerField(blank=True, null=True, verbose_name='Телеграм-ID')
    phone = models.CharField(max_length=16, blank=True, null=True, verbose_name='Телефон')
    birthdate = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name='Дата рождения', blank=True, null=True)
    subscribe_is_active = models.BooleanField(default=False, verbose_name='Подписка активна')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        default_related_name = 'users'
