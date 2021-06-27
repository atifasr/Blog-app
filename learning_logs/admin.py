from learning_logs.views import comment_add
from django.contrib import admin

# Register your models here.

from .models import topic, entry, Comment,likes,Category


class topicAdmin(admin.ModelAdmin):
    list_display = ('user', 'article_name', 'date_added')

class entryAdmin(admin.ModelAdmin):
    list_display = ('user','topic', 'text', 'date_added','picture')

class likesAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')

admin.site.register(entry,entryAdmin)
admin.site.register(topic, topicAdmin)
admin.site.register(Comment)
admin.site.register(likes,likesAdmin)
admin.site.register(Category,CategoryAdmin)

# admin.site.register(student)
