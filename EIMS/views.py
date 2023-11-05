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
from django.contrib.auth.decorators import login_required
from .validators import validate_password
from django.core.exceptions import ValidationError

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

        # Create a new user using object.create
        user = NewUser.objects.create_user(email=email, username=username, password=password)
        user.givenname = givenname
        user.surname = surname

        user.is_verified = True
        user.is_active = True
        user.is_personal = True

        user.save()

        # Log in the new user
        login(request, user)
        messages.success(request, 'Signup successful!')
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
                return redirect('signin')

            except NewUser.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
                return redirect('signin')

    context = {}
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
def dashboard(request):
    return render(request, 'app_pages/dashboard.html')

class ExpenditureinDetail(DetailView):
    model = Expenditure
    template_name = 'app_pages/expenditure-in-details.html'

class CreateExp(SuccessMessageMixin, CreateView):
    model = Expenditure
    form_class = ExpenditureForm
    template_name = "app_pages/new-exp.html"

    success_message = "Expenditure was added successfully"

    def form_valid(self, ExpenditureForm):
        ExpenditureForm.instance.uploaded_by = self.request.user
        return super().form_valid(ExpenditureForm)

class UpdateExp(SuccessMessageMixin, UpdateView):
    model = Expenditure
    template_name = 'app_pages/update_exp.html'
    fields = ['date','expense_category','vendor_payee','description','amount']

    success_message = "Expenditure was updated successfully"

def allExpRecords(request):
    allexp = Expenditure.objects.all()

    context = {
        'allexp' : allexp,
    }

    return render(request, 'app_pages/allexp-records.html', context)

def signout(request):
    logout(request)
    messages.success(request, 'Logged out successfully...!')
    return redirect('signin')