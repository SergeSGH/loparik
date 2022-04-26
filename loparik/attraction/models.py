from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Topic(models.Model):
    name = models.CharField(
        'Название топика',
        help_text='Название топика',
        max_length=20
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Топик'
        verbose_name_plural = '  Топики'

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
        verbose_name='Подтопики',
        help_text='Подтопик'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Подтопик'
        verbose_name_plural = ' Подтопики'

    def __str__(self):
        return self.name


class Message(models.Model):
    title = models.TextField(
        'Заголовок абзаца',
        help_text='Заголовок абзаца'
    )
    message = models.TextField(
        'Абзац',
        help_text='Абзац'
    )
    subtopic = models.ForeignKey(
        SubTopic,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Подтопик',
        help_text='Подтопик'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Абзац'
        verbose_name_plural = 'Абзацы'

    def __str__(self):
        return self.title[:15]
