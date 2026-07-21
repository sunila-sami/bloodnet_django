from django.contrib import admin

from .models import Recipient, RecipientDocument


class RecipientDocumentInline(admin.TabularInline):
    model = RecipientDocument
    extra = 0
    readonly_fields = ("file_name", "file_size", "uploaded_at")


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "user",
        "blood_group",
        "city",
        "is_completed",
        "created_at",
    )
    list_filter = ("is_completed", "blood_group", "gender", "city")
    search_fields = ("full_name", "user__email", "phone_number", "city")
    inlines = [RecipientDocumentInline]


@admin.register(RecipientDocument)
class RecipientDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "file_name",
        "recipient",
        "document_type",
        "file_size",
        "uploaded_at",
    )
    list_filter = ("document_type", "uploaded_at")
    search_fields = ("file_name", "recipient__full_name", "recipient__user__email")
