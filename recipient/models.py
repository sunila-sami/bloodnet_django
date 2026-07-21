from django.conf import settings
from django.db import models


class Recipient(models.Model):
    GENDER_CHOICES = (
        ("Female", "Female"),
        ("Male", "Male"),
        ("Other", "Other"),
    )

    BLOOD_GROUP_CHOICES = (
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipient_profile",
    )

    # Personal Information
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=25)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="Female")
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, default="A+")
    address = models.TextField()
    city = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to="recipient/profiles/", null=True, blank=True)

    # Medical Information
    medical_condition = models.CharField(max_length=255, blank=True)
    hospital = models.CharField(max_length=255, blank=True)
    treating_physician = models.CharField(max_length=150, blank=True)
    emergency_contact = models.CharField(max_length=150, blank=True)

    # Status
    is_completed = models.BooleanField(default=False)
    membership_since = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Recipient: {self.full_name or self.user.email} ({self.blood_group})"


class RecipientDocument(models.Model):
    DOCUMENT_TYPES = (
        ("prescription", "Prescription"),
        ("lab_report", "Laboratory Report"),
        ("medical_certificate", "Medical Certificate"),
        ("other", "Other Document"),
    )

    recipient = models.ForeignKey(
        Recipient,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPES, default="prescription")
    file = models.FileField(upload_to="recipient/documents/")
    file_name = models.CharField(max_length=255)
    file_size = models.IntegerField(default=0)  # size in bytes
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.file_name}"

    @property
    def formatted_file_size(self):
        if self.file_size < 1024:
            return f"{self.file_size} B"
        elif self.file_size < 1024 * 1024:
            return f"{self.file_size / 1024:.1f} KB"
        else:
            return f"{self.file_size / (1024 * 1024):.1f} MB"

    @property
    def is_pdf(self):
        return self.file_name.lower().endswith(".pdf") or (self.file and self.file.name.lower().endswith(".pdf"))
