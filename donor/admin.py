from django.contrib import admin

from .models import Donor, DonorBloodRequest


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "user",
        "blood_group",
        "city",
        "is_available",
        "total_donations",
        "lives_saved",
        "is_completed",
    )
    list_filter = ("is_available", "is_completed", "blood_group", "city")
    search_fields = ("full_name", "user__email", "phone_number", "city")


@admin.register(DonorBloodRequest)
class DonorBloodRequestAdmin(admin.ModelAdmin):
    list_display = (
        "patient_name",
        "hospital_name",
        "blood_group",
        "urgency_level",
        "status",
        "accepted_by",
        "created_at",
    )
    list_filter = ("urgency_level", "status", "blood_group")
    search_fields = ("patient_name", "hospital_name", "city")
