from django.contrib import admin
from django.contrib.auth.models import Group

from allauth.socialaccount.models import SocialApp, SocialToken, SocialAccount
from rest_framework.authtoken.models import TokenProxy

# Register your models here.


admin.site.index_title = "Reddit API"
admin.site.site_header = "Reddit Admin"
admin.site.site_title = "Reddit Administration"

admin.site.unregister(Group)

admin.site.unregister(TokenProxy)

admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)
