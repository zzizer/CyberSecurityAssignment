from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, DeleteView
)
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Expenditure, NewUser, OTP
from django.contrib.auth import login, logout, authenticate
from .forms import ExpenditureForm
from .utils import generate_and_send_otp
import re
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .validators import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.views import PasswordChangeView, PasswordChangeForm
from .forms import SetNewPasswordForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
# from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from .decorators import check_password_expiry, generate_access_code
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode

@login_required
def set_new_password(request):
    if request.method == 'POST':
        form = SetNewPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully.')
            return redirect('dashboard')
    else:
        form = SetNewPasswordForm(request.user)

    return render(request, 'accounts/set_new_password.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = NewUser.objects.get(pk=uid)

        # Check if the token is valid
        if default_token_generator.check_token(user, token):
            # Log the user in and redirect to the password reset form
            login(request, user)
            return redirect('set_new_password')
        else:
            messages.error(request, 'Invalid or expired token.')
            return redirect('signin')
    except (TypeError, ValueError, OverflowError, NewUser.DoesNotExist):
        messages.error(request, 'Invalid user or token.')
        return redirect('signin')

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = NewUser.objects.filter(email=email).first()

            if user:
                # Generate a unique token
                token = default_token_generator.make_token(user)

                # Create a link with the token
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = f"{request.scheme}://{request.get_host()}/password-reset-confirmed/{uidb64}/{token}/"

                # Send the link to the user via email
                subject = 'Password Reset Link'
                message = f'Use the following link to reset your password: {reset_link}'
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = [user.email]

                send_mail(subject, message, from_email, to_email)

                messages.success(request, 'Check your email for the password reset link.')
                return redirect('signin')
            else:
                messages.error(request, 'No user with that email address.')
    else:
        form = PasswordResetForm()

    return render(request, 'accounts/password_reset.html', {'form': form})


def profile(request, id):
    this_user = NewUser.objects.get(id=id)

    user = request.user

    if OTP.objects.filter(user=user).exists():
        return redirect('otp_verification')

    context = {
        'thisuser':this_user,
        'days_left_for_password_to_expire': this_user.days_left_for_password_to_expire,
    }    

    return render(request, 'accounts/profile.html', context)

class PasswordsChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('dashboard')

    success_message = "Password successfully changed...!"
    login_url = 'signin'

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        givenname = request.POST['given_name']
        surname = request.POST['surname']
        password = request.POST['password']

        # Check if the username meets the requirements
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,10}$', username):
            messages.error(request, 'Invalid username. Username must be 8-10 characters and contain a mix of alpha-numeric characters.')
            return redirect('signup')

        # Validate the password
        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, e)
            return redirect('signup')

        # Ensure that the email and username are unique
        if NewUser.objects.filter(email=email).exists() or NewUser.objects.filter(username=username).exists():
            messages.error(request, 'Email or username already exists.')
            return redirect('signup')

        access_code = generate_access_code()

        # Create a new user
        user = NewUser.objects.create_user(email=email, username=username, password=password)
        user.givenname = givenname
        user.surname = surname
        user.is_verified = False
        user.is_active = True
        user.is_personal = True
        user.access_code = access_code

        user.save()

        # Send an email to the user
        send_mail(
            'Account Registration',
            f'Thank you for registering! Your access code is: {access_code}',
            'EIMS@cyberassignment.com',
            [email],
            fail_silently=False,
        )

        login(request, user)
        messages.success(request, 'Signup successful! An email has been sent with your access code.')
        return redirect('dashboard')

    return render(request, 'accounts/up.html')


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = NewUser.objects.filter(email=email).first()

        if user is not None and user.check_password(password):
            if user.failed_login_attempts >= 3:
                messages.error(request, 'Your account is blocked. Please contact the admin for further assistance.')
                return redirect('signin')

            # If the user enters the correct credentials, generate and send OTP
            generate_and_send_otp(user)
            user.failed_login_attempts = 0  # Reset login attempts to zero
            user.save()
            
            if user.password_has_expired():
                messages.warning(request, 'Your password has expired. Please reset your password.')
                return redirect('password_reset')  # Redirect to the password reset page

            login(request, user)
            return redirect('otp_verification')  # Redirect to OTP verification page

        else:
            try:
                user = NewUser.objects.get(email=email)
                user.failed_login_attempts += 1
                user.save()
                if user.failed_login_attempts >= 3:
                    user.is_active = False
                    user.is_verified = False
                    user.save()
                    messages.error(request, 'Your account is blocked. Please contact the admin for further assistance.')
                else:
                    if user.failed_login_attempts == 2:
                        messages.error(request, 'Invalid email or password. One more incorrect attempt will result in blocking your account.')
                    else:
                        messages.error(request, 'Invalid email or password.')
                
                # Retrieve the days left for password to expire
                days_left_for_password_to_expire = user.days_left_for_password_to_expire
                messages.info(request, f'Days left for password to expire: {days_left_for_password_to_expire} days')

                return redirect('signin')

            except NewUser.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
                return redirect('signin')

    context = {

    }

    return render(request, 'accounts/in.html', context)


@login_required
def otp_verification(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        user = request.user
        otp = OTP.objects.get(user=user)

        if otp.code == entered_otp:
            login(request, user)
            otp.delete()
            return redirect('dashboard')  # Redirect to the dashboard or the desired page
        else:
            return render(request, 'otp_verification.html', {'error_message': 'Invalid OTP'})

    return render(request, 'accounts/otp_verification.html')

@login_required
@check_password_expiry
def dashboard(request):
    user = request.user

    if request.method == 'POST':
        submitted_access_code = request.POST.get('access_code')
        record_id = request.GET.get('record_id')

        if submitted_access_code == user.access_code:
            messages.success(request, 'Access code verified successfully.')

            # Redirect to 'update-exp' with the id of the specific record
            return redirect('create-exp', pk=record_id)
        else:
            messages.error(request, 'Invalid access code.')
            return redirect('dashboard')

    if OTP.objects.filter(user=user).exists():
        return redirect('otp_verification')

    return render(request, 'app_pages/dashboard.html')

class ExpenditureinDetail(LoginRequiredMixin, DetailView):
    model = Expenditure
    template_name = 'app_pages/expenditure-in-details.html'

    login_url = 'signin'

class CreateExp(LoginRequiredMixin,SuccessMessageMixin, CreateView):
    model = Expenditure
    form_class = ExpenditureForm
    template_name = "app_pages/new-exp.html"

    success_message = "Expenditure was added successfully"

    def form_valid(self, ExpenditureForm):
        ExpenditureForm.instance.uploaded_by = self.request.user
        return super().form_valid(ExpenditureForm)

class UpdateExp(LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    model = Expenditure
    template_name = 'app_pages/update_exp.html'
    fields = ['date','expense_category','vendor_payee','description','amount']

    success_message = "Expenditure was updated successfully"

    login_url = 'signin'

@login_required(login_url='signin')
def allExpRecords(request):
    user = request.user

    if request.method == 'POST':
        submitted_access_code = request.POST.get('access_code')
        record_id = request.GET.get('record_id')

        if submitted_access_code == user.access_code:
            messages.success(request, 'Access code verified successfully.')

            # Redirect to 'update-exp' with the id of the specific record
            return redirect('update-exp', pk=record_id)
        else:
            messages.error(request, 'Invalid access code.')
            return redirect('allexp')

    if OTP.objects.filter(user=user).exists():
        return redirect('otp_verification')

    allexp = Expenditure.objects.all()

    context = {
        'allexp': allexp,
    }

    return render(request, 'app_pages/allexp-records.html', context)

@login_required(login_url='signin')
def signout(request):
    logout(request)
    messages.success(request, 'Logged out successfully...!')
    return redirect('signin')