from django import forms


class CalculatorForm(forms.Form):
    months = forms.IntegerField(min_value=1, max_value=12, help_text='число месяцев')
    holidays = forms.IntegerField(min_value=1, max_value=365,
                                  help_text='число праздников и выходных')
    warm_days = forms.IntegerField(min_value=1, max_value=365, help_text='число теплых дней')
    leasing1st = forms.IntegerField(min_value=1, max_value=500000, help_text='аванс аренды, руб')
    leasing = forms.IntegerField(min_value=1, max_value=500000, help_text='аренда в месяц, руб.')
    pop_bass = forms.IntegerField(min_value=0, required=False, help_text='численность населения')


class CalculatorRybForm(forms.Form):
    months = forms.IntegerField(min_value=1, max_value=12, help_text='число месяцев')
    holidays = forms.IntegerField(min_value=1, max_value=365,
                                  help_text='число праздников и выходных')
    warm_days = forms.IntegerField(min_value=1, max_value=365, help_text='число теплых дней')
    leasing1st = forms.IntegerField(min_value=1, max_value=500000, help_text='аванс аренды, руб')
    leasing = forms.IntegerField(min_value=1, max_value=500000, help_text='аренда в месяц, руб.')
    pop_bass = forms.IntegerField(min_value=0, help_text='стоимость бассейна, руб.')
