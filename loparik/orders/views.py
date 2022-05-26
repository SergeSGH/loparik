from __future__ import absolute_import
from django.shortcuts import redirect, render

from attraction.models import Topic
from .forms import OrderForm
from .tasks import order_created


def order_create(request):
    form = OrderForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        dest_email = 'ssprihodko@gmail.com'
        subject = 'Новая заявка на консультацию'
        email_text = (
            f"Имя: {form.cleaned_data['first_name']}\n"
            + f"Фамилия: {form.cleaned_data['second_name']}\n"
            + f"е-мейл: {form.cleaned_data['email']}\n"
            + f"Комментарий: {form.cleaned_data['comment']}\n"
        )
        order_created.delay(dest_email, subject, email_text)
        return redirect('/order_create_success/')
    template = 'orders/order_create.html'
    topic_objects = []
    topics = Topic.objects.all()
    item = 13
    for one_topic in topics:
        st_list = one_topic.subtopics.all()
        item += 1
        topic_objects.append({
            'topic': one_topic, 'st_list': st_list, 'item': item
        })
    upper_menu_list = [{
        'title': 'Заявка на консультацию',
        'link': None
    }]
    context = {
        'form': form,
        'upper_menu_list': upper_menu_list,
        'topic_objects': topic_objects,
        'st_list': 'st_list'
    }
    return render(request, template, context)


def order_create_success(request):
    template = 'orders/order_create_success.html'
    topic_objects = []
    topics = Topic.objects.all()
    item = 13
    for one_topic in topics:
        st_list = one_topic.subtopics.all()
        item += 1
        topic_objects.append({
            'topic': one_topic, 'st_list': st_list, 'item': item
        })
    upper_menu_list = [{
        'title': 'Заявка на консультацию',
        'link': None
    }]
    context = {
        'upper_menu_list': upper_menu_list,
        'topic_objects': topic_objects,
        'st_list': 'st_list'
    }
    return render(request, template, context)
