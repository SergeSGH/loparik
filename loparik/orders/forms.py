from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'first_name',
            'second_name',
            'email',
            'phone',
            'comment'
        )
        help_texts = {
            'first_name': 'Имя',
            'second_name': 'Фамилия',
            'email': 'Е-мэйл',
            'phone': 'Номер телефона',
            'comment': 'Добавьте комментарий'
        }
