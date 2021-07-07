from django.contrib import admin

from products.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display_links = ['pk']
    list_display = ['pk', 'title', 'parent', ]
