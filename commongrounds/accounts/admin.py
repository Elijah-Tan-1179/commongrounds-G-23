from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Role


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline,]


class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'display_name', 'email_address']
    filter_horizontal = ['roles']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Profile, ProfileAdmin)