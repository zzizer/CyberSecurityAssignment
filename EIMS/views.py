from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, DeleteView
)
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Expenditure

def signin(request):
    return render(request, 'accounts/in.html')

def dashboard(request):
    return render(request, 'app_pages/dashboard.html')

class ExpenditureinDetails(DetailView):
    model = Expenditure
    template_name = 'app_pages/expenditure-in-details.html'