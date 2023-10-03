import uuid
from django.db import models

from common.choices import THREAD_TYPES
from common.constants import FieldConstants, ThreadType
from core.models import BaseModel
from users.models.user import User

# Create your models here.


class Thread(BaseModel):
    uid = models.UUIDField(
        verbose_name="Thread ID", unique=True, default=uuid.uuid4
    )
    name = models.CharField(max_length=FieldConstants.MAX_NAME_LENGTH)
    thread_type = models.CharField(
        max_length=8, choices=THREAD_TYPES, default=ThreadType.PRIVATE
    )
    initiated_by = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, related_name="initiated_chats"
    )
    sent_to = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, related_name="received_chats"
    )
    accepted_by_receiver = models.BooleanField(blank=True, null=True)

    class Meta:
        verbose_name = "Thread"
        verbose_name_plural = "Threads"


class Message(BaseModel):
    thread = models.ForeignKey(to=Thread, on_delete=models.CASCADE)
    sender = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_messages",
    )
    receiver = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="received_messages",
    )
    replied_to = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="replies",
        help_text="Used for replying on a previous message",
    )
    text = models.TextField()

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        constraints = [
            models.UniqueConstraint(
                fields=["sender", "receiver"], name="sender_receiver_unique"
            )
        ]
