from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin.models import LogEntry
from accounts.models import HostProfile

User = get_user_model()  # Get the user model

# Register your models here.

class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff','is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )
    ordering = ('email',)
    filter_horizontal = []

    def delete_model(self, request, obj):
        """
        Override the delete_model method to clean up associated log entries.
        """
        # Delete associated log entries for this user
        LogEntry.objects.filter(user_id=obj.pk).delete()

        # Call the superclass method to delete the user
        super().delete_model(request, obj)

@admin.register(HostProfile)
class HostUserProfileAdmin(admin.ModelAdmin):
    list_display = ("user","organization")



admin.site.register(User, CustomUserAdmin)