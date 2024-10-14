from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, username, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)
    
    def create_host_user(self, email, username, password=None, **extra_fields):
        """
        Creates and returns a host user who can modify events.
        """
        extra_fields.setdefault('is_host', True)  # Assign host privileges
        return self.create_user(email, username, password, **extra_fields)
    

class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)  # Email is unique
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    image = models.ImageField(upload_to='media/user_images', null=True, blank=True)
        
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Email is the unique identifier
    REQUIRED_FIELDS = ['username']  # Required fields when creating a user

    def __str__(self):
        return self.email
    


class HostProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    organization = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.user.username} - {self.organization}"


