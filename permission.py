from rest_framework.permissions import BasePermission,IsAdminUser


class V1IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        is_admin = request.META.get('HTTP_X_SUPER_ADMIN')
        if is_admin =="false":
            return False
        return True