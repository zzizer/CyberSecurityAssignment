from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, DeleteView
)
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Expenditure, NewUser
from django.contrib.auth import login, logout, authenticate
from .forms import ExpenditureForm
from .models import OTP
from .utils import generate_and_send_otp
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        myUser = authenticate(request, email=email, password=password)

        if myUser is not None:
            # Generate and send OTP here
            generate_and_send_otp(myUser)
            login(request, myUser)
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
                    # Generate and send OTP here
                    generate_and_send_otp(user)
                    return redirect('otp_verification')  # Redirect to OTP verification page

            except NewUser.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
                return redirect('signin')

    context = {
        # 'messages': messages,
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