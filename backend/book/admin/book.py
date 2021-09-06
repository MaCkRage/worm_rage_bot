from django.contrib import admin

from book.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'title',)
    search_fields = ('telegram_id', )
    ordering = ('title', )
