from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import BloodRequestForm
from .models import BloodRequest


def index(request):
    return render(request, "core/index.html")


@login_required
def blood_request(request):

    if request.method == "POST":

        form = BloodRequestForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            blood_request = form.save(commit=False)

            blood_request.requester = request.user

            if request.POST.get("action") == "draft":
                blood_request.status = "draft"
                messages.success(request, "Blood request draft saved successfully!")
            else:
                blood_request.status = "pending"
                messages.success(request, "Blood request submitted successfully!")

            blood_request.save()

            return redirect("core:my_requests")

    else:
        form = BloodRequestForm()

    return render(
        request,
        "core/blood_request.html",
        {
            "form": form
        }
    )


@login_required
def edit_blood_request(request, pk):
    blood_request_obj = get_object_or_404(BloodRequest, pk=pk, requester=request.user)

    if request.method == "POST":
        form = BloodRequestForm(
            request.POST,
            request.FILES,
            instance=blood_request_obj
        )

        if form.is_valid():
            blood_request_saved = form.save(commit=False)

            if request.POST.get("action") == "draft":
                blood_request_saved.status = "draft"
                messages.success(request, "Blood request draft updated successfully!")
            else:
                blood_request_saved.status = "pending"
                messages.success(request, "Blood request updated and submitted successfully!")

            blood_request_saved.save()
            return redirect("core:my_requests")
    else:
        form = BloodRequestForm(instance=blood_request_obj)

    return render(
        request,
        "core/blood_request.html",
        {
            "form": form,
            "is_edit": True,
            "blood_request": blood_request_obj
        }
    )


@login_required
def cancel_blood_request(request, pk):
    if request.method == "POST":
        blood_request_obj = get_object_or_404(BloodRequest, pk=pk, requester=request.user)
        
        if blood_request_obj.status not in ["completed", "cancelled"]:
            blood_request_obj.status = "cancelled"
            blood_request_obj.save()
            messages.success(request, "Blood request cancelled successfully!")
        else:
            messages.error(request, "This blood request cannot be cancelled.")
            
    return redirect("core:my_requests")


@login_required
def my_requests(request):

    requests = BloodRequest.objects.filter(
        requester=request.user
    ).order_by("-created_at")

    return render(
        request,
        "core/my_requests.html",
        {
            "requests": requests
        }
    )