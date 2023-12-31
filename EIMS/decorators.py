
from functools import wraps
from django.shortcuts import redirect, render
from django.contrib import messages
import random
import string

# Decorator to check password expiry
def check_password_expiry(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        # Check if the user's password has expired
        if user.password_has_expired():
            messages.error(request, "Password has expired. Please reset your password.")
            return redirect('password_reset')

        return view_func(request, *args, **kwargs)

    return _wrapped_view

def generate_access_code():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(characters, k=6))