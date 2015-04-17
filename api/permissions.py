from rest_framework import permissions

#Checking read only or admin user
class IsAuthenticatedAndIsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only admins to post or put.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:        #Methods for viewing the data
            return True
        # Write permissions are only allowed to the admin.
        return (request.user.is_authenticated() and request.user.is_superuser)