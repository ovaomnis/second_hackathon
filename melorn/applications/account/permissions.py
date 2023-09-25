from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user == obj.owner
