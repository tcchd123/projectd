from django.contrib import admin
from .models import OtpToken,User

admin.site.register(OtpToken)
admin.site.register(User)