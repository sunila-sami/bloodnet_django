from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

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
            else:
                blood_request.status = "pending"

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