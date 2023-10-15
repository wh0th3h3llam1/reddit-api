from django.contrib import admin

from chat.admin.forms import MessageAdminForm
from chat.models import Message, Participant, Room

# Register your models here.


class RoomAdmin(admin.ModelAdmin):
    list_display = ("name",)


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("user", "room")


class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "room",
        "get_message_type_display",
        "replied_to",
        "modified",
    )
    list_filter = "message_type"
    form = MessageAdminForm


admin.site.register(Room, RoomAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Message, MessageAdmin)
