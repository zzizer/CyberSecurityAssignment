from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from datetime import date
import uuid
from django.core.exceptions import ValidationError

class CustomAccountManager(BaseUserManager):

    def create_personal(self, email, username, password, **other_fields):

        other_fields.setdefault('is_verified', True)
        other_fields.setdefault('is_personal', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(email, username, password, **other_fields)

    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_verified', True)


        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff = True.'
            )
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser = True.'
            )

        return self.create_user(email, username, password, **other_fields)
    
    def create_user(self, email, username, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, password=password, **other_fields)
        
        user.set_password(password)
        user.save()
        return user

class NewUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(auto_created=True, primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    email = models.EmailField(_('Email address'), max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True)
    #complete Profile    
    givenname = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True)
    profile_photo = models.ImageField(blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    failed_login_attempts = models.IntegerField(default=0)
    date_joined = models.DateTimeField(default=timezone.now)

    #More Verification
    is_active = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_personal = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def imageURL(self):
        try:
            url = self.profile_photo.url
        except:
            url = '' #apps_images/logo.jpg
        return url

    def __str__(self):
        return f'{self.email}'
    
    class Meta:
        verbose_name  = 'New Account / User'
    

    expiration_days = 90  # Adjust this based on your requirements

    @property
    def days_until_password_expires(self):
        if self.date_joined:
            expiration_date = self.date_joined + timezone.timedelta(days=self.expiration_days)
            days_left = (expiration_date - timezone.now()).days
            return max(0, days_left)  # Ensure it's non-negative
        return 0

    @property
    def days_left_for_password_to_expire(self):
        return self.days_until_password_expires

    def password_has_expired(self):
        return self.days_until_password_expires == 0

    def clean(self):
        super().clean()
        if self.password_has_expired():
            raise ValidationError("Password has expired. Please reset your password.")

class Expenditure(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, unique=True, editable=False, default=uuid.uuid4) 
    uploaded_by = models.ForeignKey(NewUser, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField()
    expense_category = models.CharField(max_length=255)
    vendor_payee = models.CharField(max_length=255)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.date} - {self.vendor_payee}"
    
    def get_absolute_url(self):
        return reverse("allExp-records")
    
class OTP(models.Model):
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)