from django.urls import path

from . import views

app_name = "donor"

urlpatterns = [
    path("profile/", views.donor_profile_view, name="profile"),
    path("dashboard/", views.donor_dashboard_view, name="dashboard"),
    path("accept-request/<int:req_id>/", views.accept_request_view, name="accept_request"),
    path("toggle-availability/", views.toggle_availability_view, name="toggle_availability"),
]
