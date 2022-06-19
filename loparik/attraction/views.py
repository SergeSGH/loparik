import io
import itertools
import numbers

from django.http import FileResponse
from django.shortcuts import render
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .forms import CalculatorForm
from .models import MessageMain, Parameters, SubTopic, Topic


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


class row:
    def __init__(self, row_list):
        self.first = row_list[0]
        self.second = row_list[1]
        self.third = row_list[2]
        self.fourth = row_list[3]
        self.fifth = row_list[4]
        self.indent = False
        self.bold = False
        self.br = False


def format_numbers(value, digits):
    if not isinstance(value, numbers.Number):
        return value
    return '{:,.{digits}f}'.format(value, digits=digits).replace(',', ' ')
    # return f"{value:.{digits}f}"


def calculate(form=None):
    # задаем таблицу 32 x 5 для отображения
    output_table = [row(['', '', '', '', '']) for _ in range(32)]
    if form:
        # забираем данные из формы
        months = form.cleaned_data['months']
        holidays = form.cleaned_data['holidays']
        warm_days = form.cleaned_data['warm_days']
        leasing1st = form.cleaned_data['leasing1st']
        leasing = form.cleaned_data['leasing']
        params = Parameters.objects.get(pk=1)
        params.months = months
        params.holidays = holidays
        params.warm_days = warm_days
        params.leasing1st = leasing1st
        params.leasing = leasing
        params.save()
        # population = form.cleaned_data['population'] пока не используется
    else:
        params = Parameters.objects.all()[0]
        months = params.months
        holidays = params.holidays
        warm_days = params.warm_days
        leasing1st = params.leasing1st
        leasing = params.leasing
    days = months * 30  # считаем количество дней в периоде
    cold_days = days - holidays - warm_days
    # задаем первый столбец
    col_1st_list = ['Бюджет проекта', 'Мишень для шаров', 'Набор дротиков 5x2 шт.',
                    'Запас шаров (100шт. x 10)', 'Насос для шаров', 'Призы',
                    'Аренда – начальный взнос', 'ИТОГО, руб.:', '', 'РУБ.', '', '',
                    'Выручка', 'Цена билета', 'Количество билетов в день',
                    'Себестоимость шаров', 'Количество шаров', 'Себестоимость одного шара',
                    'Себестоимость призов', 'Призы (маленькие)', 'С/с приза (маленького)',
                    'Призы (средние)', 'С/с приза (среднего)', 'Призы (большие)',
                    'С/с приза (большого)', 'Зарплата оператора', 'Аренда', 'Прибыль за день',
                    '', 'количество дней', '', 'Прибыль итого']
    for i in range(32):
        output_table[i].first = col_1st_list[i]
    # устанавличаем строки с жирным шрифтом
    bold_list = [0, 7, 9, 10, 11, 12, 15, 18, 25, 26, 27, 30, 31]
    for index in bold_list:
        output_table[index].bold = True
    # строки с отступом
    indent_list = [1, 2, 3, 4, 5, 6, 13, 14, 16, 17, 19, 20, 21, 22, 23, 24, 29]
    for index in indent_list:
        output_table[index].indent = True
    # число знаков после запятой
    break_list = [7, 10, 27]
    for index in break_list:
        output_table[index].br = True
    # строки с последующим переносом
    break_list = [7, 27]
    for index in break_list:
        output_table[index].br = True
    # количество знаков после запятой
    decimal_list = [0] * 32
    # задаем строки с десятичными дробями
    one_digit_list = [19, 21, 23]
    for one_digit in one_digit_list:
        decimal_list[one_digit] = 1
    for index in break_list:
        output_table[index].br = True
    # расчет бюджета
    output_table[1].second = Parameters.objects.all()[0].target
    darts = Parameters.objects.all()[0].darts
    output_table[2].second = darts * 2
    balls = Parameters.objects.all()[0].balls
    output_table[3].second = balls * 10
    output_table[4].second = Parameters.objects.all()[0].pump
    output_table[5].second = Parameters.objects.all()[0].prize_set
    small_prize_rate = Parameters.objects.all()[0].small_prize_rate
    medium_prize_rate = Parameters.objects.all()[0].medium_prize_rate
    big_prize_rate = Parameters.objects.all()[0].big_prize_rate
    small_prize_price = Parameters.objects.all()[0].small_prize_price
    medium_prize_price = Parameters.objects.all()[0].medium_prize_price
    big_prize_price = Parameters.objects.all()[0].big_prize_price
    output_table[6].second = leasing1st
    output_table[7].second = sum([output_table[i].second for i in range(1, 7)])
    # задаем дополнительные текстовые ячейки
    output_table[9].second = 'ИТОГО'
    # output_table[10].second = '(весь период)'
    output_table[9].third = 'Праздники'
    output_table[10].third = '(за день)'
    output_table[9].fourth = 'Теплые дни'
    output_table[10].fourth = '(за день)'
    output_table[9].fifth = 'Холодные дни'
    output_table[10].fifth = '(за день)'
    output_table[30].third = '(итого)'
    output_table[30].fourth = '(итого)'
    output_table[30].fifth = '(итого)'
    # количество дней
    output_table[29].third = holidays
    output_table[29].fourth = warm_days
    output_table[29].fifth = cold_days
    # цена билета и количество в праздничные дни
    output_table[13].third = Parameters.objects.all()[0].price_hol
    output_table[14].third = Parameters.objects.all()[0].tickets_hol
    # цена билета и количество в теплые дни
    output_table[13].fourth = Parameters.objects.all()[0].price_us
    output_table[14].fourth = Parameters.objects.all()[0].tickets_us
    # цена билета и количество в холодные дни (если 0, то не работаем)
    output_table[13].fifth = Parameters.objects.all()[0].price_z
    output_table[14].fifth = Parameters.objects.all()[0].tickets_z
    # дальше считаем удельные показатели для каждого типа
    for attr in ['third', 'fourth', 'fifth']:
        # выручка
        setattr(output_table[12], attr, (getattr(output_table[13], attr)
                                         * getattr(output_table[14], attr)))
        # число шаров в день
        setattr(output_table[16], attr, (getattr(output_table[14], attr)
                                         * Parameters.objects.all()[0].balls_per_play))
        # себестоимость шара
        setattr(output_table[17], attr, balls / 100)
        # стоимость шаров в день
        setattr(output_table[15], attr, getattr(output_table[16], attr) * balls / 100)
        # количество призов каждого типа
        setattr(output_table[19], attr, getattr(output_table[14], attr) * small_prize_rate / 100)
        setattr(output_table[21], attr, getattr(output_table[14], attr) * medium_prize_rate / 100)
        setattr(output_table[23], attr, getattr(output_table[14], attr) * big_prize_rate / 100)
        # цена приза каждого типа
        setattr(output_table[20], attr, small_prize_price)
        setattr(output_table[22], attr, medium_prize_price)
        setattr(output_table[24], attr, big_prize_price)
        # общая стоимость призов
        setattr(output_table[18], attr,
                getattr(output_table[19], attr) * getattr(output_table[20], attr)
                + getattr(output_table[21], attr) * getattr(output_table[22], attr)
                + getattr(output_table[23], attr) * getattr(output_table[24], attr))

        # зарплата оператора
        if getattr(output_table[12], attr) == 0:
            setattr(output_table[25], attr, 0)
        else:
            variable = (getattr(output_table[12], attr)
                        * float(Parameters.objects.all()[0].operator_share))
            setattr(output_table[25], attr,
                    max(Parameters.objects.all()[0].operator_fix, variable))
        # аренда
        setattr(output_table[26], attr, float(leasing / 30))
        # прибыль
        print(type(getattr(output_table[12], attr)))
        print(type(getattr(output_table[15], attr)))
        print(type(getattr(output_table[18], attr)))
        print(type(getattr(output_table[25], attr)))
        print(getattr(output_table[25], attr))
        print(type(getattr(output_table[26], attr)))
        setattr(
            output_table[27], attr, getattr(output_table[12], attr)
            - getattr(output_table[15], attr) - getattr(output_table[18], attr)
            - getattr(output_table[25], attr) - getattr(output_table[26], attr)
        )
        setattr(
            output_table[31], attr,
            getattr(output_table[27], attr) * getattr(output_table[29], attr)
        )
    # считаем ИТОГО
    total_list = [12, 15, 18, 25, 26]
    for total in total_list:
        output_table[total].second = (output_table[total].third * holidays
                                      + output_table[total].fourth * warm_days
                                      + output_table[total].fifth * cold_days)
    output_table[31].second = (output_table[31].third
                               + output_table[31].fourth
                               + output_table[31].fifth)
    attrs = ['second', 'third', 'fourth', 'fifth']
    for i in range(32):
        for attr in attrs:
            setattr(output_table[i], attr,
                    format_numbers(getattr(output_table[i], attr), decimal_list[i]))
    return output_table


def subtopic(request, topic_slug, subtopic_slug):
    topic = Topic.objects.get(slug=topic_slug)
    subtopic = SubTopic.objects.get(slug=subtopic_slug)
    template = 'attraction/index.html'
    messages = subtopic.messages.all()
    topic_objects = create_topic_list(13)
    upper_menu_list = [
        {'title': 'Главная', 'link': '/'},
        {'title': topic.name, 'link': f'/{topic.slug}/'},
        {'title': subtopic.name, 'link': None},
    ]
    form = CalculatorForm(request.POST or None)
    for_calculation = False
    if subtopic_slug == 'calculator':
        for_calculation = True
    is_calculated = False
    calc_res = ''
    if request.method == 'POST' and form.is_valid():
        calc_res = calculate(form)
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
    print(topic_slug, subtopic_slug)
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
    calc_res = calculate()
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
