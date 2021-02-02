from rest_framework import permissions
from rest_framework import authentication


class HasAdminPermission(permissions.BasePermission):
    message = "Adding users not allowed."

    def has_permission(self, request, view):
        isSuperUser = request.user.is_superuser

        return isSuperUser
