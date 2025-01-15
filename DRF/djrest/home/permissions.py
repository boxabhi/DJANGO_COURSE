
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsVipUser(BasePermission):
    def has_permission(self, request, view):
        if bool(
            request.user
            and request.user.is_authenticated
            and request.user.extended.is_vip
        ):
            return True
        raise PermissionDenied("You are not a vip user")


class IsProductOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
