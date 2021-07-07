from rest_framework.permissions import BasePermission
from django.conf import settings


class OwnerWithKeyPermission(BasePermission):

    def has_permission(self, request, view):
        return request.headers.get('Owner-Key') in settings.OWNER_KEYS
