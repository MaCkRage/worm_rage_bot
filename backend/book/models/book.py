from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название книги')
    telegram_id = models.CharField(max_length=256, verbose_name='Телеграм-ID')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        default_related_name = 'books'
