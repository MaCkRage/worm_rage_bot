from django.contrib import admin

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['image', 'category', 'rating_average', 'rating_count', 'date_first_available', 'product_link', ]
    fieldsets = (
        (None,
         {'fields': ('image', 'category', 'rating_average', 'rating_count', 'date_first_available', 'product_link',)}),
    )
