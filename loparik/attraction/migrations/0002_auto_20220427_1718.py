# Generated by Django 2.2 on 2022-04-27 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attraction', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageSubTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(help_text='Заголовок абзаца', verbose_name='Заголовок абзаца')),
                ('message', models.TextField(help_text='Абзац', verbose_name='Абзац')),
                ('image', models.ImageField(upload_to='subtopic_pics/', verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Абзац',
                'verbose_name_plural': 'Абзацы',
                'ordering': ['id'],
            },
        ),
        migrations.AlterModelOptions(
            name='subtopic',
            options={'ordering': ['id'], 'verbose_name': 'Подтопик', 'verbose_name_plural': ' Подтопики'},
        ),
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ['id'], 'verbose_name': 'Топик', 'verbose_name_plural': '  Топики'},
        ),
        migrations.AlterField(
            model_name='subtopic',
            name='topic',
            field=models.ForeignKey(help_text='Подтопик', on_delete=django.db.models.deletion.CASCADE, related_name='subtopics', to='attraction.Topic', verbose_name='Подтопики'),
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.AddField(
            model_name='messagesubtopic',
            name='subtopic',
            field=models.ForeignKey(help_text='Подтопик', on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='attraction.SubTopic', verbose_name='Подтопик'),
        ),
    ]
