from django.contrib.auth import get_user_model
from django.db import models
from sorl.thumbnail import ImageField, get_thumbnail
from PIL import Image

User = get_user_model()


def scale_dimensions(width, height, longest_side):
    if width > height:
        if width > longest_side:
            ratio = longest_side*1./width
            return (int(width*ratio), int(height*ratio))
    elif height > longest_side:
        ratio = longest_side*1./height
        return (int(width*ratio), int(height*ratio))
    return (width, height)


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
            image.save("%s.jpg" % self.image.path.split('.')[0], format='JPEG', quality=70, optimize=True)
    
    def __str__(self):
        return self.title[:15]

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
        verbose_name = 'Абзац подтопика'
        verbose_name_plural = 'Абзацы подтопиков'

    def __str__(self):
        return self.title[:15]
