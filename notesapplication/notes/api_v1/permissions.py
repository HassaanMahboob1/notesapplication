from rest_framework import permissions


class SuperUserReadOnly(permissions.BasePermission):
    """
    SuperUserReadOnly : This Class is permission class which does
                        not allow to Super user to archive its notes,
                        any other user can archive but superuser cannot
    """

    edit_methods = ("GET", "POST", "PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return False
            return True

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user or request.user in obj.sharedwith.all():
            return True
        return False
