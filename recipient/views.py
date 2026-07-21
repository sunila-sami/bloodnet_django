import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import RecipientDocumentForm, RecipientProfileForm
from .models import Recipient, RecipientDocument


@login_required
def recipient_profile_view(request):
    profile, created = Recipient.objects.get_or_create(
        user=request.user,
        defaults={
            "full_name": request.user.full_name or request.user.email,
        },
    )

    if request.method == "POST":
        action = request.POST.get("action")

        # Document standalone upload action
        if action == "upload_doc":
            doc_form = RecipientDocumentForm(request.POST, request.FILES)
            if doc_form.is_valid():
                doc = doc_form.save(commit=False)
                doc.recipient = profile
                doc.file_name = doc.file.name.split("/")[-1]
                doc.file_size = doc.file.size
                doc.save()
                messages.success(request, "Medical document uploaded successfully.")
            else:
                for error in doc_form.errors.values():
                    messages.error(request, error.as_text())
            return redirect("recipient:profile")

        # Main profile form submission
        form = RecipientProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            recipient = form.save(commit=False)
            recipient.is_completed = True
            recipient.save()

            # Handle optional document uploads from the profile form file inputs
            for doc_type, field_name in [
                ("prescription", "upload_prescription"),
                ("lab_report", "upload_lab_report"),
                ("medical_certificate", "upload_medical_certificate"),
            ]:
                uploaded_file = request.FILES.get(field_name)
                if uploaded_file:
                    RecipientDocument.objects.create(
                        recipient=recipient,
                        document_type=doc_type,
                        file=uploaded_file,
                        file_name=uploaded_file.name,
                        file_size=uploaded_file.size,
                    )

            messages.success(request, "Your recipient profile has been completed and saved successfully!")
            return redirect("recipient:dashboard")
        else:
            messages.error(request, "Please correct the errors below to save your profile.")
    else:
        form = RecipientProfileForm(instance=profile)

    documents = profile.documents.all().order_by("-uploaded_at")

    context = {
        "form": form,
        "profile": profile,
        "documents": documents,
    }
    return render(request, "recipient/profile.html", context)


@login_required
@require_POST
def delete_document_view(request, doc_id):
    profile = get_object_or_404(Recipient, user=request.user)
    doc = get_object_or_404(RecipientDocument, id=doc_id, recipient=profile)

    # Delete physical file if exists
    if doc.file and os.path.isfile(doc.file.path):
        os.remove(doc.file.path)

    doc.delete()
    messages.success(request, "Document deleted successfully.")
    return redirect("recipient:profile")


@login_required
def recipient_dashboard_view(request):
    profile = getattr(request.user, "recipient_profile", None)

    if not profile or not profile.is_completed:
        messages.info(request, "Please complete your recipient profile before accessing the dashboard.")
        return redirect("recipient:profile")

    # Dummy recommended donors for UI presentation
    recommended_donors = [
        {
            "name": "Ahmed Khan",
            "blood_group": "A+",
            "distance": "2.5 km away",
            "match_pct": "98% MATCH",
            "status": "Available",
            "avatar": "AK",
        },
        {
            "name": "Sara Malik",
            "blood_group": "A+",
            "distance": "3.1 km away",
            "match_pct": "95% MATCH",
            "status": "Available",
            "avatar": "SM",
        },
    ]

    context = {
        "profile": profile,
        "active_requests_count": 0,
        "completed_requests_count": 0,
        "successful_matches_count": 0,
        "recommended_donors": recommended_donors,
    }
    return render(request, "recipient/dashboard.html", context)


@login_required
def request_blood_placeholder_view(request):
    return redirect("core:blood_request")

