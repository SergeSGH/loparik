from django.shortcuts import render
from .forms import OrderForm

def order_create(request):
    form = OrderForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        order = form.save(commit=False)
        order.save()
        return redirect('attraction:profile')
    return render(
        request,
        'orders/order_create.html',
        {'form': form}
    )