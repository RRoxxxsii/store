from rest_framework import permissions, status


class IsNotAuthenticated(permissions.BasePermission):
    """
    If user is authenticated, he does not have a permission
    """
    def has_permission(self, request, view):
        return bool(request.user and not request.user.is_authenticated)
