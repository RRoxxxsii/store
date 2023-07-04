from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    message = 'Редактировать запись может только автор.'

    def has_object_permission(self, request, view, instance):
        if request.method in SAFE_METHODS:
            return True

        return instance.user == request.user
