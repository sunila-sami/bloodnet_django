import re

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="BloodNet <noreply@example.com>",
)
class BloodNetAuthenticationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="member@example.com",
            password="OldPass123!",
            full_name="BloodNet Member",
            is_verified=True,
        )

    def test_login_page_has_forgot_password_and_eye_toggle(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertContains(response, reverse("accounts:password_reset"))
        self.assertContains(response, "data-password-toggle")
        self.assertContains(response, "Forgot Password?")

    def test_request_blood_button_opens_signup(self):
        response = self.client.get(reverse("core:index"))
        self.assertContains(
            response,
            f'<a class="btn btn-solid" href="{reverse("accounts:signup")}">Request Blood</a>',
            html=True,
        )

    def test_password_reset_flow_changes_password(self):
        response = self.client.post(
            reverse("accounts:password_reset"),
            {"email": self.user.email},
        )
        self.assertRedirects(response, reverse("accounts:password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Reset your BloodNet password", mail.outbox[0].subject)

        match = re.search(r"https?://testserver(/accounts/reset/[^\s]+)", mail.outbox[0].body)
        self.assertIsNotNone(match)

        response = self.client.get(match.group(1), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["validlink"])

        response = self.client.post(
            response.request["PATH_INFO"],
            {
                "new_password1": "NewSecurePass456!",
                "new_password2": "NewSecurePass456!",
            },
        )
        self.assertRedirects(response, reverse("accounts:password_reset_complete"))

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewSecurePass456!"))
