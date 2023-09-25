from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedOrIsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        print(request.user)
        if request.method in ('PUT', 'PATCH', 'DELETE'):
            return request.user.is_authenticated and (request.user == obj.owner or request.user.is_staff)
