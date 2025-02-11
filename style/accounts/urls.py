from django.urls import path
from .views import *


urlpatterns = [
    path("send_otp/", send_otp.as_view(), name="send_otp"),
    path("verify_otp/", verify_otp.as_view(), name="send_otp"),
    path("register/", verify_otp_create_user.as_view(), name="register"),
    path("resend-otp/", resend_otp.as_view(), name="resend-otp"),
    path("login/", login_user.as_view(), name="login"),
    path("logout/", logout_user.as_view(), name="logout"),
]