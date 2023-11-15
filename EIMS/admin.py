from django.contrib import admin
from .models import NewUser, OTP, PasswordHistory

admin.site.register(NewUser)
admin.site.register(OTP)
admin.site.register(PasswordHistory)
