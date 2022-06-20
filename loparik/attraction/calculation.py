import numbers

from .models import Parameters


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
    params = Parameters.objects.get(pk=1)
    if form:
        # забираем данные из формы
        months = form.cleaned_data['months']
        holidays = form.cleaned_data['holidays']
        warm_days = form.cleaned_data['warm_days']
        leasing1st = form.cleaned_data['leasing1st']
        leasing = form.cleaned_data['leasing']
        params.months = months
        params.holidays = holidays
        params.warm_days = warm_days
        params.leasing1st = leasing1st
        params.leasing = leasing
        params.save()
        # population = form.cleaned_data['population'] пока не используется
    else:
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
    output_table[1].second = params.target
    darts = params.darts
    output_table[2].second = darts * 2
    balls = params.balls
    output_table[3].second = balls * 10
    output_table[4].second = params.pump
    output_table[5].second = params.prize_set
    small_prize_rate = params.small_prize_rate
    medium_prize_rate = params.medium_prize_rate
    big_prize_rate = params.big_prize_rate
    small_prize_price = params.small_prize_price
    medium_prize_price = params.medium_prize_price
    big_prize_price = params.big_prize_price
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
    output_table[13].third = params.price_hol
    output_table[14].third = params.tickets_hol
    # цена билета и количество в теплые дни
    output_table[13].fourth = params.price_us
    output_table[14].fourth = params.tickets_us
    # цена билета и количество в холодные дни (если 0, то не работаем)
    output_table[13].fifth = params.price_z
    output_table[14].fifth = params.tickets_z
    # дальше считаем удельные показатели для каждого типа
    for attr in ['third', 'fourth', 'fifth']:
        # выручка
        setattr(output_table[12], attr, (getattr(output_table[13], attr)
                                         * getattr(output_table[14], attr)))
        # число шаров в день
        setattr(output_table[16], attr, (getattr(output_table[14], attr)
                                         * params.balls_per_play))
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
                        * float(params.operator_share))
            setattr(output_table[25], attr,
                    max(params.operator_fix, variable))
        # аренда
        setattr(output_table[26], attr, float(leasing / 30))
        # прибыль
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


def calculate_ryb(form=None):
    # задаем таблицу 28 x 5 для отображения
    output_table = [row(['', '', '', '', '']) for _ in range(28)]
    params = Parameters.objects.get(pk=2)
    if form:
        # забираем данные из формы
        months = form.cleaned_data['months']
        holidays = form.cleaned_data['holidays']
        warm_days = form.cleaned_data['warm_days']
        leasing1st = form.cleaned_data['leasing1st']
        leasing = form.cleaned_data['leasing']
        bass = form.cleaned_data['pop_bass']
        params.months = months
        params.holidays = holidays
        params.warm_days = warm_days
        params.leasing1st = leasing1st
        params.leasing = leasing
        params.bass = bass
        params.save()
    else:
        months = params.months
        holidays = params.holidays
        warm_days = params.warm_days
        leasing1st = params.leasing1st
        leasing = params.leasing
        bass = params.bass
    days = months * 30  # считаем количество дней в периоде
    cold_days = days - holidays - warm_days
    # задаем первый столбец
    col_1st_list = ['Бюджет проекта', 'Бассейн', 'Набор рыбок 200 шт.',
                    'Ведерки 8 шт.', 'Насос для бассейна', 'Призы',
                    'Аренда – начальный взнос', 'ИТОГО, руб.:', '', 'РУБ.', '', '',
                    'Выручка', 'Цена билета', 'Количество билетов в день',
                    'Себестоимость призов',
                    'Призы (средние)', 'С/с приза (среднего)', 'Призы (большие)',
                    'С/с приза (большого)', 'Зарплата оператора', 'Аренда',
                    'Техническое обслуживание', 'Прибыль за день',
                    '', 'количество дней', '', 'Прибыль итого']
    for i in range(28):
        output_table[i].first = col_1st_list[i]
    # устанавличаем строки с жирным шрифтом
    bold_list = [0, 7, 9, 10, 11, 12, 15, 20, 21, 22, 23, 27]
    for index in bold_list:
        output_table[index].bold = True
    # строки с отступом
    indent_list = [1, 2, 3, 4, 5, 6, 13, 14, 16, 17, 18, 25]
    for index in indent_list:
        output_table[index].indent = True
    # строки с последующим переносом
    break_list = [7, 23]
    for index in break_list:
        output_table[index].br = True
    # количество знаков после запятой
    decimal_list = [0] * 32
    # задаем строки с десятичными дробями
    one_digit_list = [16, 18]
    for one_digit in one_digit_list:
        decimal_list[one_digit] = 1
    for index in break_list:
        output_table[index].br = True
    # расчет бюджета
    output_table[1].second = params.bass
    output_table[2].second = params.rybka * params.num_rybok
    output_table[3].second = params.ved * params.num_ved
    output_table[4].second = params.pump
    output_table[5].second = params.prize_set
    medium_prize_rate = params.medium_prize_rate
    big_prize_rate = params.big_prize_rate
    medium_prize_price = params.medium_prize_price
    big_prize_price = params.big_prize_price
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
    output_table[26].third = '(итого)'
    output_table[26].fourth = '(итого)'
    output_table[26].fifth = '(итого)'
    # количество дней
    output_table[25].third = holidays
    output_table[25].fourth = warm_days
    output_table[25].fifth = cold_days
    # цена билета и количество в праздничные дни
    output_table[13].third = params.price_hol
    output_table[14].third = params.tickets_hol
    # цена билета и количество в теплые дни
    output_table[13].fourth = params.price_us
    output_table[14].fourth = params.tickets_us
    # цена билета и количество в холодные дни (если 0, то не работаем)
    output_table[13].fifth = params.price_z
    output_table[14].fifth = params.tickets_z
    # дальше считаем удельные показатели для каждого типа
    for attr in ['third', 'fourth', 'fifth']:
        # выручка
        setattr(output_table[12], attr, (getattr(output_table[13], attr)
                                         * getattr(output_table[14], attr)))
        # количество призов каждого типа
        setattr(output_table[16], attr, getattr(output_table[14], attr) * medium_prize_rate / 100)
        setattr(output_table[18], attr, getattr(output_table[14], attr) * big_prize_rate / 100)
        # цена приза каждого типа
        setattr(output_table[17], attr, medium_prize_price)
        setattr(output_table[19], attr, big_prize_price)
        # общая стоимость призов
        setattr(output_table[15], attr,
                getattr(output_table[16], attr) * getattr(output_table[17], attr)
                + getattr(output_table[18], attr) * getattr(output_table[19], attr))

        # зарплата оператора
        if getattr(output_table[12], attr) == 0:
            setattr(output_table[20], attr, 0)
        else:
            variable = (getattr(output_table[12], attr)
                        * float(params.operator_share))
            setattr(output_table[20], attr,
                    max(params.operator_fix, variable))
        # аренда
        setattr(output_table[21], attr, float(leasing / 30))
        setattr(output_table[22], attr, float(params.tehn / 30))
        # прибыль
        setattr(
            output_table[23], attr, getattr(output_table[12], attr)
            - getattr(output_table[15], attr) - getattr(output_table[20], attr)
            - getattr(output_table[21], attr) - getattr(output_table[22], attr)
        )
        setattr(
            output_table[27], attr,
            getattr(output_table[23], attr) * getattr(output_table[25], attr)
        )
    # считаем ИТОГО
    total_list = [12, 15, 20, 21, 22]
    for total in total_list:
        output_table[total].second = (output_table[total].third * holidays
                                      + output_table[total].fourth * warm_days
                                      + output_table[total].fifth * cold_days)
    output_table[27].second = (output_table[27].third
                               + output_table[27].fourth
                               + output_table[27].fifth)
    attrs = ['second', 'third', 'fourth', 'fifth']
    for i in range(28):
        for attr in attrs:
            setattr(output_table[i], attr,
                    format_numbers(getattr(output_table[i], attr), decimal_list[i]))
    return output_table
