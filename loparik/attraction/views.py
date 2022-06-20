import io
import itertools

from django.http import FileResponse
from django.shortcuts import render
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .calculation import calculate, calculate_ryb
from .forms import CalculatorForm, CalculatorRybForm
from .models import MessageMain, SubTopic, Topic


def create_topic_list(item):
    topics = Topic.objects.all()
    topic_objects = []
    for one_topic in topics:
        st_list = one_topic.subtopics.all()
        item += 1
        topic_objects.append({
            'topic': one_topic, 'st_list': st_list, 'item': item
        })
    return topic_objects


def index(request):
    template = 'attraction/index.html'
    messages = MessageMain.objects.all()
    topic_objects = create_topic_list(13)
    upper_menu_list = [{'title': 'Главная', 'link': None}]
    context = {
        'messages': messages,
        'upper_menu_list': upper_menu_list,
        'topic_objects': topic_objects
    }
    return render(request, template, context)


def topic(request, topic_slug):
    topic = Topic.objects.get(slug=topic_slug)
    template = 'attraction/index.html'
    messages = topic.messages.all()
    topic_objects = create_topic_list(13)
    upper_menu_list = [
        {'title': 'Главная', 'link': '/'},
        {'title': topic.name, 'link': None},
    ]
    context = {
        'messages': messages,
        'upper_menu_list': upper_menu_list,
        'topic_objects': topic_objects
    }
    return render(request, template, context)


def subtopic(request, topic_slug, subtopic_slug):
    topic = Topic.objects.get(slug=topic_slug)
    subtopic = SubTopic.objects.get(slug=subtopic_slug)
    template = 'attraction/index.html'
    messages = subtopic.messages.all()
    topic_objects = create_topic_list(13)
    print(f'{topic_slug}/{topic.subtopics.all()[0].slug}/')
    upper_menu_list = [
        {'title': 'Главная', 'link': '/'},
        {'title': topic.name, 'link': f'/{topic_slug}/{topic.subtopics.all()[0].slug}/'},
        {'title': subtopic.name, 'link': None},
    ]
    if topic_slug == Topic.objects.get(pk=1).slug:
        form = CalculatorForm(request.POST or None)
    else:
        form = CalculatorRybForm(request.POST or None)
    for_calculation = False
    if subtopic_slug[:10] == 'calculator':
        for_calculation = True
    is_calculated = False
    calc_res = ''
    if request.method == 'POST' and form.is_valid():
        if topic_slug == Topic.objects.get(pk=1).slug:
            calc_res = calculate(form)
        else:
            calc_res = calculate_ryb(form)
        is_calculated = True
    context = {
        'messages': messages,
        'upper_menu_list': upper_menu_list,
        'topic_objects': topic_objects,
        'form': form,
        'for_calculation': for_calculation,
        'calc_res': calc_res,
        'is_calculated': is_calculated,
        'topic_slug': topic_slug,
        'subtopic_slug': subtopic_slug
    }
    return render(request, template, context)


def download(request, topic_slug, subtopic_slug):

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont(
        'FontPDF', 'courier_new.ttf')
    )
    pdfmetrics.registerFont(TTFont(
        'FontPDFBold', 'courier_new_bold.ttf')
    )
    if topic_slug == Topic.objects.get(pk=1).slug:
        calc_res = calculate()
    else:
        calc_res = calculate_ryb()
    counter = itertools.count(800, -15)
    height = next(counter)
    p.setFont('FontPDFBold', 10)
    p.drawString(20, height,
                 f'Расчет показателей. {Topic.objects.get(slug=topic_slug).name}*')
    for row in calc_res:
        height = next(counter)
        if row.bold:
            p.setFont('FontPDFBold', 10)
        else:
            p.setFont('FontPDF', 10)
        p.drawString(20 + row.indent * 10, height, row.first)
        p.drawString(220, height, row.second)
        p.drawString(300, height, row.third)
        p.drawString(380, height, row.fourth)
        p.drawString(460, height, row.fifth)
    height = next(counter)
    p.setFont('FontPDF', 8)
    p.drawString(20, height,
                 "*расчет является приблизительным и не гарантирует достижения результата")
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(
        buffer, as_attachment=True, filename='financial_plan.pdf'
    )
