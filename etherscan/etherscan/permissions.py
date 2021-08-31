from rest_framework import permissions
from django.conf import settings


class IsAllowed(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.META.get("HTTP_ACCESS_TOKEN")
            == settings.DEFAULT_ETHERSCAN_API_TOKEN
        )
