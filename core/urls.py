from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path(
        "",
        views.index,
        name="index"
    ),

    path(
        "request-blood/",
        views.blood_request,
        name="blood_request"
    ),

    path(
        "my-requests/",
        views.my_requests,
        name="my_requests"
    ),

    path(
        "request-blood/<int:pk>/edit/",
        views.edit_blood_request,
        name="edit_blood_request"
    ),

    path(
        "request-blood/<int:pk>/cancel/",
        views.cancel_blood_request,
        name="cancel_blood_request"
    ),
]