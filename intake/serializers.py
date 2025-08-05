from rest_framework import serializers

from .models import PatientIntake


class PatientIntakeSerializer(serializers.ModelSerializer):
    """
    Serializer for PatientIntake.
    Read-only fields: id, booking info, timestamps.
    """

    class Meta:
        model = PatientIntake
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "date_of_birth",
            "contact_method",
            "reason_for_visit",
            "consent",
            "booking_id",
            "booking_datetime",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "booking_id",
            "booking_datetime",
            "created_at",
        ]
