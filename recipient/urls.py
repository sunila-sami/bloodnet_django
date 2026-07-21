from django.urls import path

from . import views

app_name = "recipient"

urlpatterns = [
    path("profile/", views.recipient_profile_view, name="profile"),
    path("dashboard/", views.recipient_dashboard_view, name="dashboard"),
    path("documents/delete/<int:doc_id>/", views.delete_document_view, name="delete_document"),
    path("request-blood/", views.request_blood_placeholder_view, name="request_blood"),
]
