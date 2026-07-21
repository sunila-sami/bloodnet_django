import random

from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    """
    Custom user model for BloodNet.

    - Logs in with email instead of username.
    - is_verified / verification_otp implement Stage 1 (email OTP
      verification) from the spec.
    - identity_status implements Stage 2 (donor identity verification —
      CNIC + blood group document, approved by an admin).
    """

    ROLE_CHOICES = (
        ("donor", "Donor"),
        ("recipient", "Recipient"),
        ("patient", "Patient"),
        ("hospital", "Hospital"),
    )

    IDENTITY_STATUS_CHOICES = (
        ("not_submitted", "Not Submitted"),
        ("pending", "Pending Admin Approval"),
        ("verified", "Verified"),
        ("rejected", "Rejected"),
    )

    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="donor")

    # ---- Stage 1: email/phone OTP verification ----
    is_verified = models.BooleanField(default=False)
    verification_otp = models.CharField(max_length=6, blank=True, null=True)

    # ---- Stage 2: donor identity verification ----
    identity_status = models.CharField(
        max_length=20,
        choices=IDENTITY_STATUS_CHOICES,
        default="not_submitted",
    )
    cnic_document = models.FileField(
        upload_to="verification/cnic/", blank=True, null=True
    )
    blood_group_document = models.FileField(
        upload_to="verification/blood_group/", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def generate_otp(self):
        """Generate and store a new 6-digit OTP on this user."""
        self.verification_otp = str(random.randint(100000, 999999))
        return self.verification_otp

    @property
    def is_donor_badge_verified(self):
        """A donor is fully trusted once both stages are complete."""
        return self.is_verified and self.identity_status == "verified"
