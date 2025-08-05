from django.contrib import admin

from .models import PatientIntake


@admin.register(PatientIntake)
class PatientIntakeAdmin(admin.ModelAdmin):
    """Configure list view, filters, and search for easier data inspection."""

    list_display = (
        "first_name",
        "last_name",
        "email",
        "booking_id",
        "booking_datetime",
        "created_at",
    )
    list_filter = (
        "contact_method",
        "consent",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
    )
    readonly_fields = ("created_at",)

    fieldsets = (
        (
            "Patient Info",
            {"fields": ("first_name", "last_name", "date_of_birth", "consent")},
        ),
        ("Contact", {"fields": ("email", "phone", "contact_method")}),
        (
            "Visit & Booking",
            {"fields": ("reason_for_visit", "booking_id", "booking_datetime")},
        ),
        ("Timestamps", {"fields": ("created_at",)}),
    )
