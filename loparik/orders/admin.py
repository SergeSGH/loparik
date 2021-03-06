from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'second_name',
        'email',
        'phone',
        'comment',
    )


admin.site.register(Order, OrderAdmin)
