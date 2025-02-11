from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser

def generate_otp():
    return get_random_string(6, allowed_chars="0123456789")

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)

    def __str__(self):
        return self.username

class OtpToken(models.Model):
    email = models.EmailField(unique=True)  # OTP is linked to email, not user
    otp_code = models.CharField(max_length=6, default=generate_otp)  # Use function instead of lambda
    otp_expires_at = models.DateTimeField()

    def __str__(self):
        return f"OTP for {self.email}"
