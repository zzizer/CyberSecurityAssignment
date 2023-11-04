from django.core.exceptions import ValidationError
import re

def validate_password(value):
    if not re.match(r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{10,15}$', value):
        raise ValidationError(
            "The password must contain at least one uppercase letter, one digit, and be 10-15 characters long."
        )