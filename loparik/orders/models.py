from django.db import models


class Order(models.Model):
    first_name = models.CharField(
        'Имя заказчика',
        help_text='Имя заказчика',
        max_length=20
    )
    second_name = models.CharField(
        'Фамилия заказчика',
        help_text='Фамилия заказчика',
        max_length=20
    )
    email = models.EmailField(
        'E-mail заказчика',
        help_text='Фамилия заказчика',
        max_length=20
    )
    comment = models.TextField(
        'Комментарий',
        help_text='Комментарий'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.first_name + ' ' + self.second_name