from django.shortcuts import render
from .forms import OrderForm
from django.shortcuts import redirect
from attraction.models import Topic
from .models import Order

def order_create(request):
    form = OrderForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        #order = form.save(commit=True)
        #order.save()
        form.save()
        return redirect('/order_create_success')
    template = 'orders/order_create.html'
    topic_objects=[]
    topics = Topic.objects.all()
    item = 13
    for one_topic in topics:
        #st_list = SubTopic.objects.filter(topic=topic)
        st_list = one_topic.subtopics.all()
        item += 1
        topic_objects.append({'topic':one_topic, 'st_list':st_list, 'item':item})
    
    upper_menu_list = [
        {'title':'Заявка на консультацию',
        'link': None}
    ]
    context = {
        'form':form,
        'upper_menu_list':upper_menu_list,
        'topic_objects':topic_objects,
        'topic':'topic',
        'st_list':'st_list'
    }
    #print(subtopics)
    return render(request, template, context)

def order_create_success(request):


    template = 'orders/order_create_success.html'
    topic_objects=[]
    topics = Topic.objects.all()
    item = 13
    for one_topic in topics:
        #st_list = SubTopic.objects.filter(topic=topic)
        st_list = one_topic.subtopics.all()
        item += 1
        topic_objects.append({'topic':one_topic, 'st_list':st_list, 'item':item})
    
    upper_menu_list = [
        {'title':'Заявка на консультацию',
        'link': None}
    ]
    context = {
        'upper_menu_list':upper_menu_list,
        'topic_objects':topic_objects,
        'topic':'topic',
        'st_list':'st_list'
    }
    #print(subtopics)
    return render(request, template, context)