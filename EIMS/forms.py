from .models import Expenditure
from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class SetNewPasswordForm(PasswordChangeForm):
    pass

class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = 'date','expense_category','vendor_payee','description','amount'
        
class PasswordResetForm(forms.Form):
    email = forms.EmailField()