from gettext import ngettext
from typing import Any, List, Tuple

from django.contrib import admin, messages
from django.http.request import HttpRequest
from django.utils import timezone

from post.models import Comment, Post

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "post_type", "locked")
    list_filter = ("post_type", "locked")
    prepopulated_fields = {"slug": ("title",)}
    actions = ("lock_posts", "unlock_posts")

    def get_readonly_fields(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> List[str] | Tuple[Any, ...]:
        read_only_fields = super().get_readonly_fields(request, obj)

        # if obj is not None:
        #     read_only_fields = ("slug", "title")

        return read_only_fields

    @admin.action(description="Lock selected Posts")
    def lock_posts(self, request, queryset):
        updated = queryset.update(
            locked=True,
            last_locked_at=timezone.now(),
            last_locked_by=request.user,
        )
        self.message_user(
            request,
            ngettext(
                msgid1=f"{updated} Post locked",
                msgid2=f"{updated} Posts locked",
                n=updated,
            ),
            messages.SUCCESS,
        )

    @admin.action(description="Unlock selected Posts")
    def unlock_posts(self, request, queryset):
        updated = queryset.update(
            locked=False,
            last_unlocked_at=timezone.now(),
            last_unlocked_by=request.user,
        )
        self.message_user(
            request,
            ngettext(
                msgid1=f"{updated} Post unlocked",
                msgid2=f"{updated} Posts unlocked",
                n=updated,
            ),
            messages.SUCCESS,
        )


class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "get_text", "parent", "locked")
    list_filter = ("post", "locked")
    actions = ("lock_comments", "unlock_comments")

    def get_text(self, instance: Comment):
        return instance.text[:20]

    get_text.short_description = "Text"

    @admin.action(description="Lock selected Comment thread")
    def lock_comments(self, request, queryset):
        updated = queryset.update(
            locked=True,
            last_locked_at=timezone.now(),
            last_locked_by=request.user,
        )
        self.message_user(
            request,
            ngettext(
                msgid1=f"{updated} Comment locked",
                msgid2=f"{updated} Comments locked",
                n=updated,
            ),
            messages.SUCCESS,
        )

    @admin.action(description="Unlock selected Comment thread")
    def unlock_comments(self, request, queryset):
        updated = queryset.update(
            locked=False,
            last_unlocked_at=timezone.now(),
            last_unlocked_by=request.user,
        )
        self.message_user(
            request,
            ngettext(
                msgid1=f"{updated} Comment unlocked",
                msgid2=f"{updated} Comments unlocked",
                n=updated,
            ),
            messages.SUCCESS,
        )


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
