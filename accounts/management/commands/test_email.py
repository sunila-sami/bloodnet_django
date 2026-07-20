from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Send a test email using the current BloodNet email configuration."

    def add_arguments(self, parser):
        parser.add_argument("recipient", help="Email address that should receive the test")

    def handle(self, *args, **options):
        recipient = options["recipient"].strip()
        if "@" not in recipient:
            raise CommandError("Enter a valid recipient email address.")

        try:
            result = send_mail(
                subject="BloodNet email configuration test",
                message="Your BloodNet Gmail SMTP configuration is working.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
        except Exception as exc:
            raise CommandError(f"Email could not be sent: {exc}") from exc

        if result != 1:
            raise CommandError("The email backend did not confirm delivery.")

        self.stdout.write(self.style.SUCCESS(f"Test email sent to {recipient}."))
