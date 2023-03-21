import random
from rest_framework.views import APIView
from django.conf import settings
from authentication.serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from authentication.models import VerifyOtp
from django.core.mail import send_mail


class RegisterView(APIView):
    """
    API endpoint for register User either Employee or Manager.
    It returns success response of getting email for verify otp or error.
    """
    def post(self, request):
        # Validate user registration data with serializer
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            # Create a new user with validated data
            user = serializer.save()

            # set user activation False
            user.is_active = False
            user.save()

            # generate random otp
            otp = random.randint(1000, 9999)
            generated_otp = otp

            # Save the OTP to the database
            Otp = VerifyOtp(user=user, otp=generated_otp)
            Otp.save()

            # Send an email to the user containing the OTP
            subject = "OTP For Registration"
            message = "Here is the otp to Register your account." + str(otp)
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )

            # Return a success response.
            response = {
                    "status": True,
                    "message": "Email Sent!!Please verify otp to register your account",
                    "data": None
                }
            return Response(data=response,
                            status=status.HTTP_200_OK)  

        else:
            # Return error response with serializer errors
            response = {
                        "status": False,
                        "message": serializer.errors,
                        "data": None}
            return Response(data=response,
                            status=status.HTTP_400_BAD_REQUEST)
