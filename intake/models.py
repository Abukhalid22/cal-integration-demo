from django.db import models


class PatientIntake(models.Model):
    """
    A simple patient intake record.

    Future FHIR mapping hints:
    - Patient.name: maps to first_name + last_name
    - Patient.telecom: maps to email & phone
    - Patient.birthDate: maps to date_of_birth
    - Extensions can be used for contact_method, reason_for_visit, consent, booking info.
    """

    CONTACT_CHOICES = [
        ("email", "Email"),
        ("phone", "Phone"),
        ("sms", "SMS"),
    ]

    first_name = models.CharField(max_length=100, help_text="FHIR Patient.name.given")
    last_name = models.CharField(max_length=100, help_text="FHIR Patient.name.family")
    email = models.EmailField(help_text="FHIR Patient.telecom (system=email)")
    phone = models.CharField(
        max_length=20, help_text="FHIR Patient.telecom (system=phone)"
    )
    date_of_birth = models.DateField(help_text="FHIR Patient.birthDate")

    contact_method = models.CharField(
        max_length=10,
        choices=CONTACT_CHOICES,
        default="email",
        help_text="Preferred contact method (could map to FHIR extension)",
    )

    reason_for_visit = models.TextField(
        blank=True, help_text="Free text; could be FHIR extension or Annotation"
    )

    consent = models.BooleanField(
        default=False,
        help_text="Patient consent for data storage (could be Consent resource later)",
    )

    booking_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Cal.com ID; future mapping to Appointment.resource.id",
    )
    booking_datetime = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Cal.com booking time; future mapping to Appointment.period.start",
    )

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Record creation timestamp"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
