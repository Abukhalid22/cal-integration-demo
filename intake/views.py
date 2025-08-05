import json
from datetime import datetime

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PatientIntake
from .serializers import PatientIntakeSerializer


class PatientIntakeListCreate(APIView):
    """
    GET  /api/intakes/     → list all
    POST /api/intakes/     → create new intake
    """

    def get(self, request):
        intakes = PatientIntake.objects.all().order_by("-created_at")
        serializer = PatientIntakeSerializer(intakes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PatientIntakeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # created_at auto‑populates
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientIntakeDetail(APIView):
    """
    GET    /api/intakes/{pk}/ → retrieve one
    PUT    /api/intakes/{pk}/ → full update
    PATCH  /api/intakes/{pk}/ → partial update
    """

    def get_object(self, pk):
        return get_object_or_404(PatientIntake, pk=pk)

    def get(self, request, pk):
        intake = self.get_object(pk)
        serializer = PatientIntakeSerializer(intake)
        return Response(serializer.data)

    def put(self, request, pk):
        intake = self.get_object(pk)
        serializer = PatientIntakeSerializer(intake, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        intake = self.get_object(pk)
        serializer = PatientIntakeSerializer(intake, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name="dispatch")
class CalWebhook(APIView):
    """
    Simple webhook to receive booking data from Cal.com
    When someone books an appointment, Cal.com sends the data here
    """

    def post(self, request):
        print("WEBHOOK RECEIVED!")

        # Get the booking data from Cal.com
        data = request.data

        # Check if this is a booking creation event
        if data.get("triggerEvent") == "BOOKING_CREATED":
            payload = data.get("payload", {})

            # Extract the important info from Cal.com
            booking_id = payload.get("uid")
            booking_start = payload.get("startTime")
            attendees = payload.get("attendees", [])
            email = attendees[0].get("email") if attendees else None

            print(f"Booking: {booking_id}, Time: {booking_start}, Email: {email}")

            # Find the intake record with this email (most recent one without booking)
            if email and booking_id and booking_start:
                try:
                    intake = (
                        PatientIntake.objects.filter(
                            email=email, booking_id__isnull=True
                        )
                        .order_by("-created_at")
                        .first()
                    )

                    if intake:
                        # Update the intake with booking info
                        intake.booking_id = booking_id
                        intake.booking_datetime = booking_start
                        intake.save()
                        print(f"Updated intake {intake.id} with booking {booking_id}")

                except Exception as e:
                    print(f"Error: {e}")

        # Always return success so Cal.com knows we received it
        return Response({"status": "received"}, status=status.HTTP_200_OK)

    def get(self, request):
        """Handle Cal.com webhook ping test (GET request)"""
        print("📡 Webhook ping test received")
        return Response(
            {"message": "Webhook endpoint is working!"}, status=status.HTTP_200_OK
        )
