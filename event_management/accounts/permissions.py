from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        # Check if the object has an 'id' attribute
        if hasattr(obj, 'id'):
            # Allow access if the object ID matches the user's ID or if the user is a superuser
            if obj.id == request.user.id:
                return True
        
        # Check if the object has a 'user' attribute
        if hasattr(obj, 'user'):
            # Allow access if the logged-in user is the owner or a superuser
            if request.user == obj.user:
                return True

        # If neither condition is met, deny access
        return False
    

class IsSuperUser(BasePermission):
    """
    Custom permission to only allow superusers to access the list of host profiles.
    """
    def has_permission(self, request, view):
        # Allow access if the user is a superuser
        return request.user.is_superuser
    


class IsSuperUserOrOwner(BasePermission):
    """
    Custom permission to only allow superusers or owners to perform actions.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the object has an 'id' attribute
        if hasattr(obj, 'id'):
            # Allow access if the object ID matches the user's ID or if the user is a superuser
            if obj.id == request.user.id or request.user.is_superuser:
                return True
        
        # Check if the object has a 'user' attribute
        if hasattr(obj, 'user'):
            # Allow access if the logged-in user is the owner or a superuser
            if request.user == obj.user or request.user.is_superuser:
                return True

        # If neither condition is met, deny access
        return False

class IsSuperUserOrHost(BasePermission):
    """
    Custom permission to only allow superusers or hosts to access a view.
    """

    def has_permission(self, request, view):
        # Check if the user is a superuser
        if request.user and request.user.is_superuser:
            return True
        
        # Check if the user is a host
        if request.user and hasattr(request.user, 'hostprofile'):
            return True
        
        # Deny access if neither condition is met
        return False


from rest_framework.exceptions import ValidationError, PermissionDenied
class IsEventHost(BasePermission):
    """
    Custom permission to only allow users who are hosts and also
    the host of the event to access the event.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated (this is generally handled by IsAuthenticated)
        if not request.user.is_authenticated:
            raise PermissionDenied("User is not authenticated.")

        # Check if the user has a HostProfile
        if not hasattr(request.user, 'hostprofile'):
            raise PermissionDenied("User does not have a HostProfile.")

        # Check if the user is the host of the event
        if obj.host.user != request.user:
            raise PermissionDenied("You are not the host of this event.")

        return True