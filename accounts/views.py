import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import LoginForm, SignupForm
from .models import User

logger = logging.getLogger(__name__)


def send_otp_email(user):
    """Send the user's current OTP and return True when accepted by backend."""
    subject = "Your BloodNet verification code"
    plain_message = (
        f"Hi {user.full_name or user.email},\n\n"
        f"Your BloodNet verification code is: {user.verification_otp}\n\n"
        "Enter this code on the verification page to activate your account. "
        "If you didn't request this, you can ignore this email."
    )
    html_message = f"""
    <div style="font-family:Arial,sans-serif;max-width:560px;margin:auto;padding:28px;
                border:1px solid #f1d0d2;border-radius:16px;background:#fffafa;color:#322a2c;">
      <h2 style="margin:0 0 12px;color:#c92e38;">Verify your BloodNet account</h2>
      <p>Hi {user.full_name or user.email},</p>
      <p>Use this verification code to activate your account:</p>
      <div style="font-size:32px;font-weight:700;letter-spacing:8px;text-align:center;
                  padding:18px;margin:22px 0;border-radius:12px;background:#fff0f0;color:#c92e38;">
        {user.verification_otp}
      </div>
      <p style="color:#74686b;">If you did not request this code, you can ignore this email.</p>
    </div>
    """

    try:
        sent_count = send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
            html_message=html_message,
        )
        return sent_count == 1
    except Exception:
        # Keep the verification page usable when SMTP credentials/network fail.
        logger.exception("Could not send BloodNet OTP email to %s", user.email)
        return False


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("core:index")

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.full_name = form.cleaned_data["full_name"]
            user.role = form.cleaned_data["role"]

            user.is_verified = False
            user.generate_otp()
            user.save()

            request.session["verification_user_id"] = user.id
            send_otp_email(user)

            messages.success(
                request,
                "Account created successfully! Please verify your email address.",
            )
            return redirect("accounts:verify_account")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})


def verify_account(request):
    user_id = request.session.get("verification_user_id")
    if not user_id:
        return redirect("accounts:signup")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        request.session.pop("verification_user_id", None)
        return redirect("accounts:signup")

    error = None

    if request.method == "POST":
        entered_otp = "".join(
            request.POST.get(f"otp{i}", "").strip() for i in range(1, 7)
        )

        # Check expiration (10 minutes = 600 seconds)
        if user.otp_created_at and (timezone.now() - user.otp_created_at).total_seconds() > 600:
            error = "The verification code has expired. Please request a new one."
            user.verification_otp = None
            user.save(update_fields=["verification_otp"])
        elif len(entered_otp) == 6 and entered_otp == user.verification_otp:
            user.is_verified = True
            user.verification_otp = None
            user.otp_created_at = None
            user.save(update_fields=["is_verified", "verification_otp", "otp_created_at"])

            request.session.pop("verification_user_id", None)
            
            # Auto-login the user upon verification
            login(request, user)
            messages.success(request, "Your account is verified successfully!")

            # Role-based redirection
            if user.role in ["recipient", "patient"]:
                recipient_profile = getattr(user, "recipient_profile", None)
                if recipient_profile and recipient_profile.is_completed:
                    return redirect("recipient:dashboard")
                return redirect("recipient:profile")
            elif user.role == "donor":
                donor_profile = getattr(user, "donor_profile", None)
                if donor_profile and donor_profile.is_completed:
                    return redirect("donor:dashboard")
                return redirect("donor:profile")
            return redirect("core:index")
        else:
            error = "Invalid verification code. Please try again."

    return render(
        request,
        "accounts/verify_account.html",
        {"email": user.email, "error": error},
    )


def resend_otp(request):
    user_id = request.session.get("verification_user_id")
    if not user_id:
        return redirect("accounts:signup")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        request.session.pop("verification_user_id", None)
        return redirect("accounts:signup")

    # Check cooldown (60 seconds)
    if user.otp_sent_at and (timezone.now() - user.otp_sent_at).total_seconds() < 60:
        time_left = int(60 - (timezone.now() - user.otp_sent_at).total_seconds())
        messages.error(request, f"Please wait {time_left} seconds before requesting a new OTP.")
        return redirect("accounts:verify_account")

    user.generate_otp()
    user.save(update_fields=["verification_otp", "otp_created_at", "otp_sent_at"])

    if send_otp_email(user):
        messages.success(request, "A new verification code has been sent.")
    else:
        messages.error(
            request,
            "The code could not be emailed. Please check Gmail SMTP settings and try again.",
        )

    return redirect("accounts:verify_account")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:index")

    error = None

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].strip().lower()
            password = form.cleaned_data["password"]

            user = authenticate(request, username=email, password=password)

            if user is None:
                error = "Invalid email or password."
            elif not user.is_verified:
                request.session["verification_user_id"] = user.id
                verify_url = reverse("accounts:verify_account")
                error = f'Please verify your email address before logging in. <a href="{verify_url}" style="text-decoration: underline; color: inherit; font-weight: bold;">Verify now</a>'
            else:
                login(request, user)
                if user.role in ["recipient", "patient"]:
                    recipient_profile = getattr(user, "recipient_profile", None)
                    if recipient_profile and recipient_profile.is_completed:
                        return redirect("recipient:dashboard")
                    return redirect("recipient:profile")
                elif user.role == "donor":
                    donor_profile = getattr(user, "donor_profile", None)
                    if donor_profile and donor_profile.is_completed:
                        return redirect("donor:dashboard")
                    return redirect("donor:profile")
                return redirect("core:index")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form, "error": error})


def logout_view(request):
    logout(request)
    return redirect("core:index")
