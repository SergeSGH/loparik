from django.contrib import admin

from .models import Topic, SubTopic, MessageSubTopic, MessageTopic, MessageMain


class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'image'
    )
    search_fields = ('name',)


class SubTopicAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'topic',
        'name'
    )
    search_fields = ('name',)


class MessageMainAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'message',
        'image'
    )


class MessageTopicAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'topic',
        'title',
        'message',
        'image'
    )

class MessageSubTopicAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'subtopic',
        'title',
        'message',
        'image'
    )

admin.site.register(Topic, TopicAdmin)
admin.site.register(SubTopic, SubTopicAdmin)
admin.site.register(MessageTopic, MessageTopicAdmin)
admin.site.register(MessageSubTopic, MessageSubTopicAdmin)
admin.site.register(MessageMain, MessageMainAdmin)