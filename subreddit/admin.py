from gettext import ngettext
from django.contrib import admin, messages
from django.utils.html import format_html

from subreddit.models import Moderator, Subreddit, SubredditLink, SubredditUser

# Register your models here.


class SubredditLinkInline(admin.TabularInline):
    model = SubredditLink
    extra = 2


class SubredditAdmin(admin.ModelAdmin):
    list_display = ("name", "display_name", "owner", "nsfw")
    list_filter = ("owner", "nsfw")
    inlines = (SubredditLinkInline,)
    readonly_fields = ("about",)


class ModeratorAdmin(admin.ModelAdmin):
    list_display = ("user", "subreddit", "added_by")
    list_filter = ("subreddit",)


class SubredditUserAdmin(admin.ModelAdmin):
    list_display = ("user", "subreddit")


class SubredditLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "get_url", "subreddit")
    list_filter = ("subreddit",)
    search_fields = ("name",)
    search_help_text = "Search via Name"

    def get_url(self, instance: SubredditLink):
        return format_html(
            '<a href="{}" target="_blank">{}</a>', instance.url, instance.url
        )

    get_url.short_description = "URL"


class BannedUserAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "subreddit",
        "description",
        "banned_until",
        "banned_by",
    )
    list_filter = ("user", "subreddit", "banned_until")
    search_fields = ("description",)
    search_help_text = "Search via Description"
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
