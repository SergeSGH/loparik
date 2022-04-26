from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'first_name',
            'second_name',
            'email',
            'comment'
        )
        help_texts = {
            'first_name': 'Введите имя',
            'second_name': 'Введите фамилию',
            'email': 'Введите е-мэйл',
            'comment': 'Добавьте комментарий'
        }
