from django.shortcuts import render

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
        'topic_objects': topic_objects,
        'st_list': 'st_list'
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
        'topic_objects': topic_objects,
        'st_list': 'st_list'
    }
    return render(request, template, context)


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
    context = {
        'messages': messages,
        'upper_menu_list': upper_menu_list,
        'topic_objects': topic_objects,
        'st_list': 'st_list'
    }
    return render(request, template, context)
