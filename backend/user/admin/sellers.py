from django.contrib import admin

from user.models import Seller


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display_links = ['pk']
    list_display = ['pk', 'title', 'seller_id',]
