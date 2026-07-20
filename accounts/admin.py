from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """
    Lets an admin review Stage 2 (donor identity) submissions — CNIC and
    blood group documents — and flip identity_status to verified/rejected,
    per the LifeStream verification spec.
    """

    ordering = ("email",)
    list_display = (
        "email",
        "full_name",
        "role",
        "is_verified",
        "identity_status",
        "is_staff",
    )
    list_filter = ("role", "is_verified", "identity_status", "is_staff")
    search_fields = ("email", "full_name")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("full_name", "role")}),
        (
            "Verification",
            {
                "fields": (
                    "is_verified",
                    "verification_otp",
                    "identity_status",
                    "cnic_document",
                    "blood_group_document",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "full_name", "role", "password1", "password2"),
            },
        ),
    )
