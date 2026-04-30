from django.contrib import admin
from .models import EventType, Event, EventSignup, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username']


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'location', 'start_time', 'end_time', 'created_on']
    list_filter = ['category', 'status', 'start_time']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'start_time'
    readonly_fields = ['created_on', 'updated_on']
    # category is managed by developers only — not editable by regular users via admin
    filter_horizontal = ['organizer']


@admin.register(EventSignup)
class EventSignupAdmin(admin.ModelAdmin):
    list_display = ['event', 'user_registrant', 'new_registrant']
    list_filter = ['event']
    search_fields = ['event__title', 'user_registrant__user__username', 'new_registrant']
