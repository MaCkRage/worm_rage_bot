from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from products.models import Category


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display_links = ['pk']
    list_display = ['pk', 'title', 'parent', 'tree_actions', 'indented_title']
