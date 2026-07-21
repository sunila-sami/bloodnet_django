from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import DonorProfileForm
from .models import Donor, DonorBloodRequest


def ensure_sample_blood_requests():
    """Ensure sample recipient blood requests exist for presentation."""
    if DonorBloodRequest.objects.count() == 0:
        DonorBloodRequest.objects.create(
            patient_name="Fatima Zahra",
            hospital_name="Liaquat National Hospital",
            city="Karachi",
            blood_group="A+",
            units_needed=2,
            urgency_level="emergency",
            distance="1.8 km away",
        )
        DonorBloodRequest.objects.create(
            patient_name="Tariq Mahmood",
            hospital_name="Civil Hospital",
            city="Karachi",
            blood_group="O-",
            units_needed=1,
            urgency_level="urgent",
            distance="3.4 km away",
        )
        DonorBloodRequest.objects.create(
            patient_name="Aisha Rehman",
            hospital_name="Aga Khan University Hospital",
            city="Karachi",
            blood_group="A+",
            units_needed=2,
            urgency_level="emergency",
            distance="4.2 km away",
        )


@login_required
def donor_profile_view(request):
    profile, created = Donor.objects.get_or_create(
        user=request.user,
        defaults={
            "full_name": request.user.full_name or request.user.email,
        },
    )

    if request.method == "POST":
        form = DonorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            donor = form.save(commit=False)
            donor.is_completed = True
            donor.save()

            messages.success(
                request, "Your donor profile has been completed and saved successfully!"
            )
            return redirect("donor:dashboard")
        else:
            messages.error(
                request, "Please correct the errors below to save your profile."
            )
    else:
        form = DonorProfileForm(instance=profile)

    context = {
        "form": form,
        "profile": profile,
    }
    return render(request, "donor/profile.html", context)


@login_required
def donor_dashboard_view(request):
    profile = getattr(request.user, "donor_profile", None)

    if not profile or not profile.is_completed:
        messages.info(
            request, "Please complete your donor profile before accessing the dashboard."
        )
        return redirect("donor:profile")

    ensure_sample_blood_requests()

    # Available pending requests for this donor to accept
    available_requests = DonorBloodRequest.objects.filter(status="pending").order_by("-created_at")

    # Requests already accepted by this donor
    accepted_requests = DonorBloodRequest.objects.filter(
        accepted_by=profile
    ).order_by("-accepted_at")

    context = {
        "profile": profile,
        "available_requests": available_requests,
        "accepted_requests": accepted_requests,
    }
    return render(request, "donor/dashboard.html", context)


@login_required
@require_POST
def accept_request_view(request, req_id):
    profile = get_object_or_404(Donor, user=request.user)
    blood_req = get_object_or_404(DonorBloodRequest, id=req_id)

    if blood_req.status == "accepted":
        messages.warning(request, "This blood request has already been accepted.")
        return redirect("donor:dashboard")

    blood_req.status = "accepted"
    blood_req.accepted_by = profile
    blood_req.accepted_at = timezone.now()
    blood_req.save()

    # Update donor stats
    profile.total_donations += 1
    profile.lives_saved += 1
    profile.save(update_fields=["total_donations", "lives_saved"])

    messages.success(
        request,
        f"Thank you! You have accepted the blood request for {blood_req.patient_name} at {blood_req.hospital_name}.",
    )
    return redirect("donor:dashboard")


@login_required
@require_POST
def toggle_availability_view(request):
    profile = get_object_or_404(Donor, user=request.user)
    profile.is_available = not profile.is_available
    profile.save(update_fields=["is_available"])

    status_str = "AVAILABLE" if profile.is_available else "UNAVAILABLE"
    messages.success(request, f"Your status has been updated to: {status_str}.")
    return redirect("donor:dashboard")
