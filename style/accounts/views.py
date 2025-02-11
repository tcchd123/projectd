from django.contrib.auth import get_user_model, login, logout
from django.utils import timezone
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import APIView, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import OtpToken
import random

User = get_user_model()

# Generate OTP and send it via email
@permission_classes([AllowAny])
class send_otp(APIView):
    def post(self,request):
        """ Generates and sends an OTP for email verification before user creation """
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Remove any existing OTPs for this email
        OtpToken.objects.filter(email=email).delete()

        # Generate a new OTP
        otp_code = str(random.randint(100000, 999999))  # 6-digit OTP
        otp = OtpToken.objects.create(email=email, otp_code=otp_code, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))

        # Send OTP email
        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP code is {otp.otp_code}. It expires in 5 minutes.",
            from_email="your-email@gmail.com",
            recipient_list=[email],
            fail_silently=False
        )

        return Response({"message": "OTP sent to email"}, status=status.HTTP_200_OK)

@permission_classes([AllowAny])
class verify_otp(APIView):
    def post(self,request):
        
        email = request.data.get("email")
        otp_code = request.data.get("otp_code")

        otp = OtpToken.objects.filter(email=email).last()

        if not otp or otp.otp_expires_at < timezone.now():
            return Response({"error": "OTP expired or invalid"}, status=status.HTTP_400_BAD_REQUEST)

        if otp.otp_code != otp_code:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Delete OTP after successful verification
        otp.delete()

        return Response({"message": "User loged successfully"}, status=status.HTTP_201_CREATED)


# Verify OTP and Create User
@permission_classes([AllowAny])
class verify_otp_create_user(APIView):
    def post(self,request):
        """ Verifies OTP and creates the user after successful verification """
        email = request.data.get("email")
        otp_code = request.data.get("otp_code")
        username = request.data.get("username")
        password = request.data.get("password")

        otp = OtpToken.objects.filter(email=email).last()

        if not otp or otp.otp_expires_at < timezone.now():
            return Response({"error": "OTP expired or invalid"}, status=status.HTTP_400_BAD_REQUEST)

        if otp.otp_code != otp_code:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        # OTP verified, create user
        user = User.objects.create_user(email=email, username=username, password=password)
        
        # Delete OTP after successful verification
        otp.delete()

        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

# Resend OTP
@permission_classes([AllowAny])
class resend_otp(APIView):
    def post(self ,request):
        """ Resends a new OTP to the email """
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Remove old OTPs
        OtpToken.objects.filter(email=email).delete()

        # Generate and send new OTP
        otp_code = str(random.randint(100000, 999999))
        otp = OtpToken.objects.create(email=email, otp_code=otp_code, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))

        send_mail(
            subject="Resend OTP",
            message=f"Your new OTP is {otp.otp_code}. It expires in 5 minutes.",
            from_email="your-email@gmail.com",
            recipient_list=[email],
            fail_silently=False
        )

        return Response({"message": "New OTP sent"}, status=status.HTTP_200_OK)

# Login User
@permission_classes([AllowAny])
class login_user(APIView):

    """
    API view for user login. It returns a JWT token upon successful authentication.
    """

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        # Validate input
        if not email or not password:
            raise ValidationError("email and password are required fields.")

        # Authenticate user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid username or password.")

        # Manually hash and check the password
        if not check_password(password, user.password):
            raise AuthenticationFailed("Invalid password.")

        # Create JWT token
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Return the tokens in response
        return Response(
            {
                'user':user.username,
                'refresh': str(refresh),
                'access': str(access_token),
            }, 
            status=status.HTTP_200_OK
        )

# Logout User
@permission_classes([IsAuthenticated])
class logout_user(APIView):
    def post(self , request):
        """ Logs out the authenticated user """
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
