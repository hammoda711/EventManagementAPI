from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HostListView, HostProfileViewSet, UserListView, UserProfileView, RegistrationView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,TokenBlacklistView

router = DefaultRouter()
router.register(r'host-profile', HostProfileViewSet, basename='host-profile')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegistrationView.as_view(), name='register'),
    #using simplejwt views for auth
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('user/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('hosts/', HostListView.as_view(), name='host-list'),

]

