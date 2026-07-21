from django.contrib import admin
from .models import BloodRequest


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "requester",
        "blood_component",
        "units_required",
        "required_date",
        "urgency_level",
        "city",
        "status",
        "created_at",
    )

    list_filter = (
        "blood_component",
        "urgency_level",
        "status",
        "city",
    )

    search_fields = (
        "requester__email",
        "hospital_or_blood_bank",
        "city",
        "area",
    )

    ordering = (
        "-created_at",
    )