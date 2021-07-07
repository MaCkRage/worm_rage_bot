from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from django.db import models

from app.mixins import UpdateFieldsMixin
from products.models.product import Product
from user.models.seller import Seller


class Price(UpdateFieldsMixin):
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Цена')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, blank=True, verbose_name='Продавец',
                               related_name='sellers_prices')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, verbose_name='Товар',
                                related_name='product_prices')

    objects = models.Manager()
    bulk_update_or_create = BulkUpdateOrCreateQuerySet.as_manager()

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'
        default_related_name = 'prices'

    def __str__(self):
        return f'{self.seller} {self.product} {self.price}'
