from django.contrib import admin

from .models import Topic, SubTopic, Message


class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name'
    )
    search_fields = ('name',)


class SubTopicAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'topic',
        'name'
    )
    search_fields = ('name',)


class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'subtopic',
        'title',
        'message'
    )

admin.site.register(Topic, TopicAdmin)
admin.site.register(SubTopic, SubTopicAdmin)
admin.site.register(Message, MessageAdmin)