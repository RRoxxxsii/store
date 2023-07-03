from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAnAuthor(BasePermission):
    message = 'Редактировать запись может только автор.'

    class IsOwnerOrReadOnly(BasePermission):
        def has_object_permission(self, request, view, obj):
            if request.method in SAFE_METHODS:
                return True

            return obj.customer == request.user
