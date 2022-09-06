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
