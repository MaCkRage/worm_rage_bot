from django.contrib import admin

from products.models import Price


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display_links = ['pk']
    list_display = ['pk', 'price', 'seller', 'product', ]
