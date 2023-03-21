import random
from rest_framework.views import APIView
from django.conf import settings
from authentication.serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from authentication.models import VerifyOtp
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token


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


class VerifyOtpView(APIView):
    """
    API endpoint for verification of registered User.
    It returns success response of verify otp or error.
    """
    def post(self, request):

        # Retrieve the otp entered by user
        user_otp = request.data.get('otp')

        # check if the user not entered data
        if user_otp is None:
            response = {
                        "status": False,
                        "message": "Provide OTP!!",
                        "data": None
                    }
            return Response(data=response,
                            status=status.HTTP_400_BAD_REQUEST)

        # Get the VerifyOtp object with the given OTP
        if VerifyOtp.objects.filter(otp=user_otp).exists():
            otp = VerifyOtp.objects.get(otp=user_otp)
            user = otp.user

            # If user is verified then set user activation status to True
            if user:
                user.is_active = True
                user.save()

                # Delete the otp so further reuse of otp is not possible
                otp.delete()

                # Return a success response.
                response = {
                            "status": True,
                            "message": "OTP Verified!!Registration is successfull!!"
                        }
                return Response(data=response,
                                status=status.HTTP_200_OK)
        else:
            # If the OTP is incorrect, return an error message
            response = {
                        "status": False,
                        "message": "OTP is incorrect!!",
                        "data": None
                    }
            return Response(data=response,
                            status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API view for user login.User can be authenticated using email and password.
    If user is verified then get token key otherwise get error.
    """
    def post(self, request):

        # Getting the detail entered by user
        email = request.data.get("email")
        password = request.data.get("password")

        # check if the user not entered data
        if email is None or password is None:
            response = {
                        "status": False,
                        "message": "Provide email and password",
                        "data": None
                    }
            return Response(data=response,
                            status=status.HTTP_400_BAD_REQUEST)

        # Login logic using AuthTokenSerializer
        if User.objects.filter(email=email).exists():
            username = User.objects.get(email=email).username
            data = {
                "username": username,
                "password": password
            }
            serializer = AuthTokenSerializer(data=data)
            if serializer.is_valid():
                user = serializer.validated_data['user']

                # generate or get token for user
                token, _ = Token.objects.get_or_create(user=user)

                # Return success response
                response = {
                    "status": True,
                    "message": "Login is Successful!!",
                    "token": token.key,
                }
                return Response(data=response, status=status.HTTP_202_ACCEPTED)
            else:
                response = {
                    "status": False,
                    "message": "Provide correct email and password",
                    "data": None,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ForgetPasswordView(APIView):
    """
    API endpoint for Forget password.
    It returns success response of email getting otp or error message.
    """
    def post(self, request):

        # retrieve email id entered by user
        email = request.data.get('email')

        # Check if email was provided in the request
        if email is None:
            response = {
                    "status": False,
                    "message": "Provide email address!!",
                    "data": None
                }
            return Response(data=response,
                            status=status.HTTP_200_OK)

        # Check if a user with that email exists
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            # Generate a random 4-digit OTP and save it in the database
            otp = random.randint(1000, 9999)
            generated_otp = otp

            # Save the OTP to the database
            Forget_password = VerifyOtp(user=user, otp=generated_otp)
            Forget_password.save()

            # Send an email to the user containing the OTP
            subject = "Forget password"
            message = "Here is the otp to Reset your password." + str(otp)
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
                    "message": "Email sent to Reset your password!!"
                }
            return Response(data=response,
                            status=status.HTTP_200_OK)
        else:
            # If no user with that email exists, return an error message
            response = {
                        "status": False,
                        "message": "Provide correct email id!!",
                        "data": None
                    }
            return Response(data=response,
                            status=status.HTTP_400_BAD_REQUEST)