from django import forms
from .models import Reports  # Import your Reports model

class ReportForm(forms.ModelForm):
    class Meta:
        model = Reports
        fields = ['title', 'description']  # List the fields you want to include in the form

from .models import Budget

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'start_date', 'end_date']

        # forms.py
from django import forms
from .models import UserSpendingCategory

class SpendingCategoryForm(forms.ModelForm):
    class Meta:
        model = UserSpendingCategory
        fields = ['name']
