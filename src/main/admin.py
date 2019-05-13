from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_active', 'is_agent',
                    'phone_number', 'screen_name',)
    list_filter = ('email', 'is_active',
                   'is_agent', 'phone_number', 'screen_name',)
    fieldsets = (
        (None, {'fields': ('email', 'password',
                           'is_active', 'last_login', 'screen_name',)}),
        ('Types', {'fields': ('is_staff', 'is_agent', 'is_superuser',)}),
        ('Permsissions', {'fields': ('user_permissions',)}),
        ('Groups', {'fields': ('groups',)}),
        ('Agents', {'fields': ('image', 'phone_number',)})
    )

    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1',
                                                 'password2', 'is_staff', 'is_agent', 'is_active',)})
    )

    search_fields = ('email', 'phone_number',)
    ordering = ('email', 'phone_number')


admin.site.register(CustomUser, CustomUserAdmin)
