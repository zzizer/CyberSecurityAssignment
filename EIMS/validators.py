import re
from django.core.exceptions import ValidationError

def validate_password(value):
    if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_])[A-Za-z\d\W_]{10,40}$', value):
        raise ValidationError(
            "The password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character. It should be 10-40 characters long."
        )