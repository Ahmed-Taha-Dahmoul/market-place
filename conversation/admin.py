from django.contrib import admin
from .models import Notification, Message, Conversation

admin.site.register(Notification)
admin.site.register(Message)
admin.site.register(Conversation)

