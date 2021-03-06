# Generated by Django 2.2 on 2022-04-27 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attraction', '0003_messagetopic'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='image',
            field=models.ImageField(blank=True, upload_to='topic_pics/', verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='messagesubtopic',
            name='image',
            field=models.ImageField(blank=True, upload_to='subtopic_pics/', verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='messagetopic',
            name='image',
            field=models.ImageField(blank=True, upload_to='topic_pics/', verbose_name='Картинка'),
        ),
    ]
