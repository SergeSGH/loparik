from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Topic(models.Model):
    name = models.CharField(
        'Название топика',
        help_text='Название топика',
        max_length=20
    )
    slug = models.SlugField(
        'Слаг',
        help_text='Слаг',
        unique=True
    )
    image = models.ImageField(
        'Картинка',
        upload_to='topic_pics/',
        blank=True
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Топик'
        verbose_name_plural = '   Топики'

    def __str__(self):
        return self.name


class SubTopic(models.Model):
    name = models.CharField(
        'Название подтопика',
        help_text='Название подтопика',
        max_length=20
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
        verbose_name_plural = ' Подтопики'

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
        verbose_name_plural = '   Абзацы главной страницы'

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
        verbose_name_plural = '  Абзацы топиков'

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
        verbose_name = 'Абзац'
        verbose_name_plural = 'Абзацы'

    def __str__(self):
        return self.title[:15]
