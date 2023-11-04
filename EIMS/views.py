from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, DeleteView
)
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Expenditure
from django.contrib.auth import login, logout, authenticate
from .forms import ExpenditureForm

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        myUser = authenticate(request, email=email, password=password)

        if myUser is not None:
            login(request, myUser)
            myUser.failed_login_attempts = 0
            myUser.save()
            messages.success(request, 'Successfully Logged In...!')
            return redirect('dashboard')

        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('signin')

    context = {
        messages: 'messages',
    }
    return render(request, 'accounts/in.html', context)

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