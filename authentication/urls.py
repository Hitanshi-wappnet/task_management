from django.urls import path
from authentication import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name='register'),
    path("verifyotp/", views.VerifyOtpView.as_view(), name='verifyotp'),
    path("login/", views.LoginView.as_view(), name='login'),
    path("forgetpassword/", views.ForgetPasswordView.as_view(),
         name="forgetpassword")
]
