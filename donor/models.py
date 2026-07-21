from django.conf import settings
from django.db import models


class Donor(models.Model):
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
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
        related_name="donor_profile",
    )

    # Personal Details
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=25)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="Male")
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, default="A+")
    address = models.TextField()
    city = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to="donor/profiles/", null=True, blank=True)

    # Donation Status & Stats
    is_available = models.BooleanField(default=True)
    last_donation_date = models.DateField(null=True, blank=True)
    total_donations = models.PositiveIntegerField(default=0)
    lives_saved = models.PositiveIntegerField(default=0)

    # Metadata
    is_completed = models.BooleanField(default=False)
    membership_since = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Donor: {self.full_name or self.user.email} ({self.blood_group})"


class DonorBloodRequest(models.Model):
    URGENCY_CHOICES = (
        ("emergency", "EMERGENCY"),
        ("urgent", "URGENT"),
        ("normal", "NORMAL"),
    )

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("completed", "Completed"),
    )

    patient_name = models.CharField(max_length=150)
    hospital_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100, default="Karachi")
    blood_group = models.CharField(max_length=5, choices=Donor.BLOOD_GROUP_CHOICES, default="A+")
    units_needed = models.PositiveIntegerField(default=1)
    urgency_level = models.CharField(max_length=20, choices=URGENCY_CHOICES, default="emergency")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    distance = models.CharField(max_length=50, default="2.5 km away")

    accepted_by = models.ForeignKey(
        Donor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="accepted_requests",
    )
    accepted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Blood Request #{self.id} — {self.blood_group} for {self.patient_name}"
