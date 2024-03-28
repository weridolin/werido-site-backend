from rest_framework.permissions import BasePermission,IsAdminUser,IsAuthenticated
from rest_framework import exceptions

class V1IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        is_admin = request.META.get('HTTP_X_SUPER_ADMIN')
        if is_admin =="false":
            raise exceptions.PermissionDenied('user is not super admin')
        return True