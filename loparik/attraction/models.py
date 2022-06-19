from django.contrib.auth import get_user_model
from django.db import models
from sorl.thumbnail import ImageField
from PIL import Image

User = get_user_model()


def scale_dimensions(width, height, longest_side):
    if width > height:
        if width > longest_side:
            ratio = longest_side * 1. / width
            return (int(width * ratio), int(height * ratio))
    elif height > longest_side:
        ratio = longest_side * 1. / height
        return (int(width * ratio), int(height * ratio))
    return (width, height)


class Parameters(models.Model):
    months = models.IntegerField('Число месяцев', help_text='мес.')
    holidays = models.IntegerField('Число праздников и выходных', help_text='дней')
    warm_days = models.IntegerField('Число теплых дней', help_text='дней')
    leasing1st = models.IntegerField('Аванс аренды', help_text='руб.')
    leasing = models.IntegerField('Аренда', help_text='руб.')
    target = models.IntegerField('Стоимость мишени', help_text='руб.')
    darts = models.IntegerField('Стоимость набора дротиков', help_text='руб.')
    balls = models.IntegerField('Стоимость набора шаров', help_text='руб.')
    pump = models.IntegerField('Стоимость насоса', help_text='руб.')
    prize_set = models.IntegerField('Стоимость запаса призов', help_text='руб.')
    price_hol = models.IntegerField('Цена билета в праздники', help_text='руб.')
    price_us = models.IntegerField('Цена билета в обычный день', help_text='руб.')
    price_z = models.IntegerField('Цена билета в плохой день', help_text='руб.')
    tickets_hol = models.IntegerField('Количество билетов в праздники', help_text='шт.')
    tickets_us = models.IntegerField('Количество билетов в обычный день', help_text='шт.')
    tickets_z = models.IntegerField('Количество билетов в плохой день', help_text='шт.')
    balls_per_play = models.IntegerField('Количество шаров на игру', help_text='шт.')
    small_prize_rate = models.IntegerField('% маленьких призов на 100 игр',
                                           help_text='шт. на 100 игр')
    medium_prize_rate = models.IntegerField('% средних призов на 100 игр',
                                            help_text='шт. на 100 игр')
    big_prize_rate = models.IntegerField('% больших призов на 100 игр',
                                         help_text='шт. на 100 игр')
    small_prize_price = models.IntegerField('цена маленького приза',
                                            help_text='цена маленького приза')
    medium_prize_price = models.IntegerField('цена среднего приза',
                                             help_text='цена среднего приза')
    big_prize_price = models.IntegerField('цена большого приза',
                                          help_text='цена большого приза')
    operator_fix = models.IntegerField('Фикс. ставка оператора в день', help_text='руб.')
    operator_share = models.DecimalField('Доля от выручки оператора', decimal_places=2,
                                         max_digits=3, help_text='доля')

    class Meta:
        ordering = ['id']
        verbose_name = 'Набор параметров для расчета'
        verbose_name_plural = 'Наборы параметров для расчета'


class Topic(models.Model):
    name = models.CharField(
        'Название топика',
        help_text='Название топика',
        max_length=50
    )
    slug = models.SlugField(
        'Слаг',
        help_text='Слаг',
        unique=True
    )
    image = ImageField(
        'Картинка',
        upload_to='topic_pics/',
        blank=True
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            image = Image.open(self.image.path)
            (width, height) = image.size
            (new_width, new_height) = scale_dimensions(width, height, longest_side=40)
            if new_width < width or new_height < height:
                image = image.resize((new_width, new_height))
            image.save("%s.jpg" % self.image.path.split('.')[0],
                       format='JPEG', quality=70, optimize=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Топик'
        verbose_name_plural = '    Топики'

    def __str__(self):
        return self.name


class SubTopic(models.Model):
    name = models.CharField(
        'Название подтопика',
        help_text='Название подтопика',
        max_length=50
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='subtopics',
        verbose_name='Топик',
        help_text='Топик'
    )
    slug = models.SlugField(
        'Слаг',
        help_text='Слаг',
        unique=True
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Подтопик'
        verbose_name_plural = '  Подтопики'

    def __str__(self):
        return self.name


class MessageMain(models.Model):
    title = models.TextField(
        'Заголовок на главной странице',
        help_text='Заголовок на главной странице'
    )
    message = models.TextField(
        'Абзац на главной странице',
        help_text='Абзац на главной странице',
        blank=True
    )
    image = models.ImageField(
        'Картинка',
        upload_to='main_pics/',
        blank=True
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Абзац главной страницы'
        verbose_name_plural = '    Абзацы главной страницы'

    def __str__(self):
        return self.title[:15]


class MessageTopic(models.Model):
    title = models.TextField(
        'Заголовок абзаца',
        help_text='Заголовок абзаца'
    )
    message = models.TextField(
        'Абзац топика',
        help_text='Абзац топика',
        blank=True
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Топик',
        help_text='Топик'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='topic_pics/',
        blank=True
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Абзац топика'
        verbose_name_plural = '   Абзацы топиков'

    def __str__(self):
        return self.title[:15]


class MessageSubTopic(models.Model):
    title = models.TextField(
        'Заголовок абзаца',
        help_text='Заголовок абзаца'
    )
    message = models.TextField(
        'Абзац подтопика',
        help_text='Абзац подтопика',
        blank=True
    )
    subtopic = models.ForeignKey(
        SubTopic,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Подтопик',
        help_text='Подтопик'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='subtopic_pics/',
        blank=True
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Абзац подтопика'
        verbose_name_plural = ' Абзацы подтопиков'

    def __str__(self):
        return self.title[:15]
