from django.contrib import admin

from .models import MessageMain, MessageSubTopic, MessageTopic, SubTopic, Topic
from django.utils.safestring import mark_safe

class TopicAdmin(admin.ModelAdmin):
    def image_img(self, obj):
        if obj.image:
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="40"/></a>'.format(obj.image.url))
        else:
            return '(Нет изображения)'
    image_img.short_description = 'Картинка'
    
    list_display = (
        'id',
        'name',
        'slug',
        'image',
        'image_img'
    )
    search_fields = ('name',)


class SubTopicAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'topic',
        'name',
        'slug'
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
