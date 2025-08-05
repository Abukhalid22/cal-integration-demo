from django.urls import path

from .views import CalWebhook, PatientIntakeDetail, PatientIntakeListCreate

urlpatterns = [
    path("intakes/", PatientIntakeListCreate.as_view(), name="intake-list-create"),
    path("intakes/<int:pk>/", PatientIntakeDetail.as_view(), name="intake-detail"),
    path(
        "webhook/cal/", CalWebhook.as_view(), name="cal-webhook"
    ),  # Cal.com webhook endpoint
]
