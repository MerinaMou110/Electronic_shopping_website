from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'email', 'name', 'tc', 'role', 'is_active','is_staff')
    list_filter = ('role', 'is_active')
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'first_name', 'last_name', 'tc')}),
        ('Permissions', {'fields': ('role', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'first_name', 'last_name', 'tc', 'password1', 'password2', 'role', 'is_active'),
        }),
    )
    search_fields = ('email', 'name', 'first_name', 'last_name')
    ordering = ('email', 'id')
    filter_horizontal = ()

# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)
