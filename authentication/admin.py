from django.contrib import admin
from authentication.models import VerifyOtp


# Registation of Forget Password Model
@admin.register(VerifyOtp)
class VerifyOtpAdmin(admin.ModelAdmin):
    fields = ["user", "otp"]
