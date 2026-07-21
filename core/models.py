from django.conf import settings
from django.db import models


class BloodRequest(models.Model):

    BLOOD_COMPONENT_CHOICES = [
        ("whole_blood", "Whole Blood"),
        ("red_cells", "Red Blood Cells"),
        ("platelets", "Platelets"),
        ("plasma", "Plasma"),
        ("cryoprecipitate", "Cryoprecipitate"),
    ]

    URGENCY_CHOICES = [
        ("routine", "Routine"),
        ("urgent", "Urgent"),
        ("emergency", "Emergency"),
    ]

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("pending", "Pending"),
        ("matching", "Matching Donors"),
        ("matched", "Donor Matched"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blood_requests"
    )

    blood_component = models.CharField(
        max_length=30,
        choices=BLOOD_COMPONENT_CHOICES,
        default="whole_blood"
    )

    units_required = models.PositiveIntegerField(
        default=1
    )

    required_date = models.DateField()

    urgency_level = models.CharField(
        max_length=20,
        choices=URGENCY_CHOICES,
        default="routine"
    )

    hospital_or_blood_bank = models.CharField(
        max_length=255
    )

    city = models.CharField(
        max_length=100
    )

    area = models.CharField(
        max_length=100
    )

    additional_details = models.TextField(
        blank=True
    )

    medical_document = models.FileField(
        upload_to="blood_requests/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.requester} - "
            f"{self.get_blood_component_display()} - "
            f"{self.get_urgency_level_display()}"
        )