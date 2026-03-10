from django.contrib import admin

from .models import Commission, CommissionType

# register com type model
@admin.register(CommissionType)
class CommissionTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

# register com req model
@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "people_required",
        "created_on",
    )

    search_fields = ("title",)