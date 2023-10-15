from django.utils.translation import gettext_lazy as _

from model_utils.choices import Choices

from common.constants import MessageType, PostType, ThreadType


POST_TYPES = Choices(
    (PostType.TEXT, _("Text")),
    (PostType.IMAGE, _("Image")),
    (PostType.VIDEO, _("Video")),
    (PostType.LINK, _("Link")),
)


FEED_TYPES = Choices(
    ("subscribed", "Subscribed"),
    ("popular", "Popular"),
    ("all", "All"),
)


THREAD_TYPES = Choices(
    (ThreadType.PRIVATE, "Private"),
    (ThreadType.GROUP, "Group"),
    (ThreadType.CHANNEL, "Channel"),
)


MESSAGE_TYPES = Choices(
    (MessageType.TEXT, _("Text")),
    (MessageType.IMAGE, _("Image")),
    (MessageType.VIDEO, _("Video")),
    (MessageType.GIF, _("GIF")),
    (MessageType.FILE, _("File")),
)
