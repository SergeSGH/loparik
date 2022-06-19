from django import forms


class CalculatorForm(forms.Form):
    months = forms.IntegerField(min_value=1, max_value=12)
    holidays = forms.IntegerField(min_value=1, max_value=365)
    warm_days = forms.IntegerField(min_value=1, max_value=365)
    leasing1st = forms.IntegerField(min_value=1, max_value=500000)
    leasing = forms.IntegerField(min_value=1, max_value=500000)
    population = forms.IntegerField(min_value=0, required=False)
