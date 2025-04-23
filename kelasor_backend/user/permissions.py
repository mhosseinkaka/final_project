from rest_framework.permissions import BasePermission

class IsSupport(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'support':
            return True
        else:
            return False

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'superuser':
            return True
        else:
            return False