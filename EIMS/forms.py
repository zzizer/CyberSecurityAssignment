from .models import Expenditure
from django import forms

class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = '__all__'