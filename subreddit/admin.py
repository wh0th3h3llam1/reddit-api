from gettext import ngettext
from django.contrib import admin, messages

from subreddit.models import (
    BannedUser,
    Moderator,
    Subreddit,
    SubredditLink,
    SubredditUser,
)

# Register your models here.


class SubredditLinkInline(admin.TabularInline):
    model = SubredditLink
    extra = 2


class SubredditAdmin(admin.ModelAdmin):
    list_display = ("name", "display_name", "owner", "nsfw")
    list_filter = ("owner", "nsfw")
    search_fields = ("name", "display_name")
    inlines = (SubredditLinkInline,)
    readonly_fields = ("about",)


class ModeratorAdmin(admin.ModelAdmin):
    list_display = ("user", "subreddit", "added_by")
    list_filter = ("subreddit",)


class SubredditUserAdmin(admin.ModelAdmin):
    list_display = ("user", "subreddit", "created")
    list_filter = ("subreddit",)
    search_fields = ("user__username",)


class SubredditLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "subreddit")
    list_filter = ("subreddit",)


class BannedUserAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "subreddit",
        "description",
        "banned_until",
        "banned_by",
    )
    list_filter = ("user", "subreddit", "banned_until")
    actions = ("unban_users",)

    @admin.action(description="Unban selected Users")
    def unban_users(self, request, queryset):
        updated = queryset.delete()
        self.message_user(
            request,
            ngettext(
                singular=f"{updated} user unbanned",
                plural=f"{updated} users unbanned",
                number=updated,
            ),
            messages.SUCCESS,
        )


admin.site.register(Subreddit, SubredditAdmin)
admin.site.register(SubredditUser, SubredditUserAdmin)
admin.site.register(Moderator, ModeratorAdmin)
admin.site.register(SubredditLink, SubredditLinkAdmin)
admin.site.register(BannedUser, BannedUserAdmin)
