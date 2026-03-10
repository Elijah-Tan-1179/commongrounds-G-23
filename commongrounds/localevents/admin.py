from django.contrib import admin
from .models import EventType, Event


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    list_filter = ['name']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title',
                    'category',
                    'location',
                    'start_time',
                    'end_time',
                    'created_on']
    list_filter = ['category', 'start_time', 'created_on']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'start_time'
    readonly_fields = ['created_on', 'updated_on']
