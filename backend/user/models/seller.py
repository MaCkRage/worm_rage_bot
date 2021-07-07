from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from django.db import models

from app.mixins import UpdateFieldsMixin


class Seller(UpdateFieldsMixin):
    title = models.CharField(max_length=120, verbose_name='Название')
    seller_id = models.CharField(max_length=120, blank=True, null=True, verbose_name='ID')

    objects = models.Manager()
    bulk_update_or_create = BulkUpdateOrCreateQuerySet.as_manager()

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'
        default_related_name = 'sellers'

    def __str__(self):
        return f'{self.title}'
