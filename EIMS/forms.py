from .models import Expenditure
from django import forms

class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = 'date','expense_category','vendor_payee','description','amount'