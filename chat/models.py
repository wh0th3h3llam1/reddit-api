from __future__ import annotations
from typing import TYPE_CHECKING
import uuid

from django.db import models
from django.utils.functional import cached_property

from common.choices import MESSAGE_TYPES
from common.constants import FieldConstants, MessageType
from common.utils import get_chat_attachment_path
from core.models import BaseModel
from users.models.user import User

if TYPE_CHECKING:
    from django.db.models import Manager

# Create your models here.


# class Thread(BaseModel):
#     uid = models.UUIDField(
#         verbose_name="Thread ID", unique=True, default=uuid.uuid4
#     )
#     name = models.CharField(max_length=FieldConstants.MAX_NAME_LENGTH)
#     thread_type = models.CharField(
#         max_length=8, choices=THREAD_TYPES, default=ThreadType.PRIVATE
#     )
#     initiated_by = models.ForeignKey(
#         to=User, on_delete=models.SET_NULL, related_name="initiated_chats"
#     )
#     sent_to = models.ForeignKey(
#         to=User, on_delete=models.SET_NULL, related_name="received_chats"
#     )
#     accepted_by_receiver = models.BooleanField(blank=True, null=True)

#     class Meta:
#         verbose_name = "Thread"
#         verbose_name_plural = "Threads"


# class Message(BaseModel):
#     thread = models.ForeignKey(to=Thread, on_delete=models.CASCADE)
#     sender = models.ForeignKey(
#         to=User,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name="sent_messages",
#     )
#     receiver = models.ForeignKey(
#         to=User,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name="received_messages",
#     )
#     replied_to = models.ForeignKey(
#         to="self",
#         on_delete=models.SET_NULL,
#         blank=True,
#         null=True,
#         related_name="replies",
#         help_text="Used for replying on a previous message",
#     )
#     text = models.TextField()

#     class Meta:
#         verbose_name = "Message"
#         verbose_name_plural = "Messages"
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["sender", "receiver"], name="sender_receiver_unique"
#             )
#         ]


class Room(BaseModel):
    uid = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=FieldConstants.MAX_NAME_LENGTH)
    is_active = models.BooleanField(default=True)

    participants: Manager["Participant"]
    messages: Manager["Message"]

    def __str__(self) -> str:
        return self.name or self.id

    @cached_property
    def get_participants_count(self) -> int:
        return self.participants.count()


class Participant(BaseModel):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="rooms"
    )
    room = models.ForeignKey(
        to=Room, on_delete=models.CASCADE, related_name="participants"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "room"], name=_("user_room_unique")
            )
        ]

    def __str__(self) -> str:
        return f"{self.user} - {self.room}"


class Message(BaseModel):
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name="messages",
        blank=True,
        null=True,
    )
    room = models.ForeignKey(
        to=Room, on_delete=models.CASCADE, related_name="messages"
    )
    replied_to = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="replies",
        help_text="Used for replying on a previous message",
    )
    text = models.TextField(blank=True, null=True)
    message_type = models.CharField(
        max_length=15, choices=MESSAGE_TYPES, default=MessageType.TEXT
    )
    attachment = models.FileField(
        upload_to=get_chat_attachment_path,
        blank=True,
        null=True,
        # TODO Add all file (image, video, gif, file) validators here
        validators=[],
    )

    def __str__(self) -> str:
        return f"{self.user} - {self.room} - {self.get_message_type_display()}"

    def save(self, *args, **kwargs):
        if self.text:
            # Trimming whitespaces from the body
            self.text = self.text.strip()
        return super().save(*args, **kwargs)
