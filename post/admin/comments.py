from django.contrib import admin, messages
from django.utils import timezone
from django.utils.translation import ngettext

from post.admin.admin_forms import CommentAdminForm
from post.models import Comment

# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "post", "get_text", "parent", "locked")
    list_filter = ("post", "locked")
    actions = ("lock_comments", "unlock_comments")
    form = CommentAdminForm

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
                singular=f"{updated} Comment locked",
                plural=f"{updated} Comments locked",
                number=updated,
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
                singular=f"{updated} Comment unlocked",
                plural=f"{updated} Comments unlocked",
                number=updated,
            ),
            messages.SUCCESS,
        )


admin.site.register(Comment, CommentAdmin)
