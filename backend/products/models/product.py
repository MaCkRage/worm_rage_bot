from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from django.db import models

from app.mixins import UpdateFieldsMixin
from .category import Category


class Product(UpdateFieldsMixin):
    image = models.FileField(blank=True, null=True, upload_to='public/media/%Y/%M/%D', verbose_name="Фотография товара")
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, verbose_name='Категория', related_name='product_category')
    rating_average = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                         verbose_name='Средний рейтинг')
    rating_count = models.IntegerField(blank=True, null=True, verbose_name='Кол-во отзывов')
    date_first_available = models.DateTimeField(blank=True, null=True, verbose_name='Доступно к покупке с')
    product_link = models.CharField(max_length=240, blank=True, null=True, verbose_name='Ссылка')

    objects = models.Manager()
    bulk_update_or_create = BulkUpdateOrCreateQuerySet.as_manager()

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        default_related_name = 'products'

    def __str__(self):
        return f'Продукт {self.pk} {self.category}'
