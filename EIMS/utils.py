import secrets
from django.core.mail import send_mail
from .models import OTP

def generate_and_send_otp(user):
    # Generate a 6-digit OTP.
    otp = secrets.randbelow(1000000)
    otp = f"{otp:06d}"  # Format as a 6-digit string.

    # Save the OTP in the database.
    OTP.objects.update_or_create(user=user, defaults={'code': otp})

    # Send the OTP to the user's email.
    subject = 'Your One-Time Password'
    message = f'Your one-time password is: {otp}'
    from_email = 'your@example.com'
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)
