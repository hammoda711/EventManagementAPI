from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission to only allow users to access and modify their own profile.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the object (their own profile)
        return obj.id == request.user.id

class IsSuperUser(BasePermission):
    """
    Custom permission to only allow superusers to access the list of host profiles.
    """
    def has_permission(self, request, view):
        # Allow access if the user is a superuser
        return request.user.is_superuser
    

from rest_framework.permissions import BasePermission

class IsSuperUserOrOwner(BasePermission):
    """
    Custom permission to only allow superusers or owners to perform actions.
    """
    def has_object_permission(self, request, view, obj):
        # Allow access if the user is a superuser or the owner of the object
        return request.user.is_superuser or obj == request.user

    #def has_permission(self, request, view):
        # You can add any additional logic for general actions here if needed
    #   return True  # Allow all authenticated users to access this view
