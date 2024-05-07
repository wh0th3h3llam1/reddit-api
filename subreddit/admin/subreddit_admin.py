from django.contrib import admin, messages
from django.db.models import BooleanField, Case, F, QuerySet, When
from django.utils.html import format_html
from django.utils.translation import ngettext

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
    search_help_text = "Search via Name or Display name"
    inlines = (SubredditLinkInline,)
    readonly_fields = ("about",)


class ModeratorAdmin(admin.ModelAdmin):
    list_display = ("user", "subreddit", "added_by")
    list_filter = ("subreddit",)


class SubredditUserAdmin(admin.ModelAdmin):
    list_display = ("user", "subreddit", "is_user_a_moderator", "created")
    list_filter = ("subreddit",)  # ("is_moderator", IsModeratorAdminFilter))
    search_fields = ("user__username",)
    search_help_text = "Search via Username"
    actions = ("ban_users",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            moderator_user_id=F("subreddit__moderators__user__id"),
        ).annotate(
            is_mod=Case(
                When(
                    user_id__in=F("moderator_user_id"),
                    then=True,
                ),
                default=False,
                output_field=BooleanField(),
            )
        )

        return queryset

    def is_user_a_moderator(self, instance: SubredditUser) -> bool:
        return instance.is_moderator

    @admin.action(description="Ban Selected Users")
    def ban_users(self, request, queryset: QuerySet["SubredditUser"]):
        # Must verify that no mods are being banned
        if queryset.filter(is_mod=True).exists():
            self.message_user(
                request,
                "Some users are Moderators for their respective subreddits. They cannot be banned",
                messages.ERROR,
                fail_silently=False,
            )
        else:
            updated = self._ban_users(queryset)
            self.message_user(
                request,
                ngettext(
                    singular=f"{updated[0]} user banned",
                    plural=f"{updated[0]} users banned",
                    number=updated,
                ),
                messages.SUCCESS,
            )

    def _ban_users(self, queryset: QuerySet["SubredditUser"]):
        banned_users = [
            BannedUser(subreddit=obj.subreddit, user=obj.user)
            for obj in queryset
        ]
        created = BannedUser.objects.bulk_create(banned_users)
        return queryset.delete()

    is_user_a_moderator.short_description = "Is Moderator?"
    is_user_a_moderator.boolean = True


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
        updated = queryset.delete()[0]
        self.message_user(
            request,
            ngettext(
                singular=f"{updated} user unbanned",
                plural=f"{updated} users unbanned",
                number=updated,
            ),
            messages.SUCCESS,
        )


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
                singular=f"{updated[0]} user unbanned",
                plural=f"{updated[0]} users unbanned",
                number=updated[0],
            ),
            messages.SUCCESS,
        )


admin.site.register(Subreddit, SubredditAdmin)
admin.site.register(SubredditUser, SubredditUserAdmin)
admin.site.register(Moderator, ModeratorAdmin)
admin.site.register(SubredditLink, SubredditLinkAdmin)
admin.site.register(BannedUser, BannedUserAdmin)
