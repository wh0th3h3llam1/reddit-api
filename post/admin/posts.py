from django.contrib import admin, messages
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import ngettext

from post.admin.admin_forms import PostAdminForm
from post.models import Post

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "get_subreddit", "slug", "post_type", "locked")
    list_filter = ("post_type", "locked")
    search_fields = ("title", "slug", "body")
    search_help_text = "Search via Title, Slug or Body"
    actions = ("lock_posts", "unlock_posts")
    form = PostAdminForm

    def get_subreddit(self, instance: Post):
        link = reverse(
            "admin:subreddit_subreddit_change", args=[instance.subreddit.id]
        )
        return format_html("<a href='{}'>{}</a>", link, instance.subreddit)

    get_subreddit.short_description = "Subreddit"

    def get_prepopulated_fields(self, request, obj):
        prepoulated_fields = super().get_prepopulated_fields(request, obj)
        if obj is None:
            prepoulated_fields.update({"slug": ("title",)})

        return prepoulated_fields

    def get_readonly_fields(self, request, obj):
        read_only_fields = super().get_readonly_fields(request, obj)
        if obj is not None:
            read_only_fields += ("slug", "title")
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
                singular=f"{updated} Post locked",
                plural=f"{updated} Posts locked",
                number=updated,
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
                singular=f"{updated} Post unlocked",
                plural=f"{updated} Posts unlocked",
                number=updated,
            ),
            messages.SUCCESS,
        )


admin.site.register(Post, PostAdmin)
