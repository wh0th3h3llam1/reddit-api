from django.contrib import admin

from subreddit.models import Moderator, Subreddit, SubredditLink, SubredditUser

# Register your models here.


class SubredditLinkInline(admin.TabularInline):
    model = SubredditLink
    extra = 2


class SubredditAdmin(admin.ModelAdmin):
    list_display = ("name", "display_name", "owner", "nsfw")
    list_filter = ("owner", "nsfw")
    inlines = (SubredditLinkInline,)


class ModeratorAdmin(admin.ModelAdmin):
    list_display = ("user", "subreddit", "added_by")
    list_filter = ("subreddit",)


class SubredditUserAdmin(admin.ModelAdmin):
    list_display = ("user", "subreddit")


class SubredditLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "subreddit")
    list_filter = ("subreddit",)


admin.site.register(Subreddit, SubredditAdmin)
admin.site.register(SubredditUser, SubredditUserAdmin)
admin.site.register(Moderator, ModeratorAdmin)
admin.site.register(SubredditLink, SubredditLinkAdmin)
