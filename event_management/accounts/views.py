from rest_framework import viewsets, permissions
from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from accounts.models import HostProfile
from .serializers import HostProfileSerializer, RegistrationSerializer, UserProfileSerializer
from .permissions import IsOwner, IsSuperUser, IsSuperUserOrOwner
from rest_framework.exceptions import ValidationError
# Create your views here.


User = get_user_model()

class RegistrationView(CreateAPIView):
    """
    A viewset for registering new users.
    """
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can register

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # Create the user

        # Generate tokens for the newly created user
        token = TokenObtainPairSerializer.get_token(user)

        return Response({
            **serializer.data,
            'refresh': str(token),
            'access': str(token.access_token),
        }, status=status.HTTP_201_CREATED)



class UserProfileView(RetrieveUpdateDestroyAPIView):
    """
    Allow a user to view, update, and delete their profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    lookup_field = 'username'  # Use username for lookups


    def get_queryset(self):
            #Restrict host profile retrieval to the authenticated user only.
            return User.objects.filter(id=self.request.user.id)


    def destroy(self, request, *args, **kwargs):
        # allow superusers to delete any profile.
        self.permission_classes = [IsSuperUserOrOwner]  # Use custom permission for delete
        return super().destroy(request, *args, **kwargs)


class UserListView(ListAPIView):
    """
    allow only superuser to view all user profiles.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated,IsSuperUser]

     

class HostProfileViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing, editing, and deleting host profile instances.
    """
    serializer_class = HostProfileSerializer
    permission_classes = [IsAuthenticated,IsOwner]
    lookup_field = 'user__username' 

    def get_queryset(self):
        #allow host user to retrieve only his host profile
        return HostProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Ensure that the logged-in user is assigned to the host profile
        if HostProfile.objects.filter(user=self.request.user).exists():
            raise ValidationError("Host profile already exists.")
        serializer.save(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
      #only super user or owner can delete profile
        self.permission_classes = [IsSuperUserOrOwner] 
        return super().destroy(request, *args, **kwargs)
    

class HostListView(ListAPIView):
    """
    Allow only superuser to view all host profiles.
    """
    serializer_class = HostProfileSerializer
    permission_classes = [IsAuthenticated,IsSuperUser]

    
    def get_queryset(self):
        # Only admin can get the list of all users that have a HostProfile
        return HostProfile.objects.all()