# Generated by Django 3.1 on 2022-04-21 22:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название топика', max_length=20, verbose_name='Название топика')),
            ],
            options={
                'verbose_name': 'Топик',
                'verbose_name_plural': 'Топики',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='SubTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название подтопика', max_length=20, verbose_name='Название подтопика')),
                ('topic', models.ForeignKey(help_text='Топик', on_delete=django.db.models.deletion.CASCADE, related_name='subtopics', to='attraction.topic', verbose_name='Топик')),
            ],
            options={
                'verbose_name': 'Подтопик',
                'verbose_name_plural': 'Подтопики',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(help_text='Заголовок абзаца', verbose_name='Заголовок абзаца')),
                ('message', models.TextField(help_text='Абзац', verbose_name='Абзац')),
                ('subtopic', models.ForeignKey(help_text='Подтопик', on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='attraction.subtopic', verbose_name='Подтопик')),
            ],
            options={
                'verbose_name': 'Абзац',
                'verbose_name_plural': 'Абзацы',
                'ordering': ['-id'],
            },
        ),
    ]
