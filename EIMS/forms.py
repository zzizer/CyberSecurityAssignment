from .models import Expenditure
from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class SetNewPasswordForm(PasswordChangeForm):
    pass

class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = 'date', 'expense_category', 'vendor_payee', 'description', 'amount'

    def __init__(self, *args, **kwargs):
        super(ExpenditureForm, self).__init__(*args, **kwargs)

        # Set placeholders for each field
        self.fields['date'].widget.attrs['placeholder'] = 'year-month-day'
        self.fields['expense_category'].widget.attrs['placeholder'] = 'Expense category'
        self.fields['vendor_payee'].widget.attrs['placeholder'] = 'Vendor Payee'
        self.fields['description'].widget.attrs['placeholder'] = 'Description'
        self.fields['amount'].widget.attrs['placeholder'] = 'Amount'

class PasswordResetForm(forms.Form):
    email = forms.EmailField()