from rest_framework import permissions


class HasTempLinkPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.subscription.generate_expiring_links is True
