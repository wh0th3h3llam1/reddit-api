from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.


admin.site.index_title = "Reddit API"
admin.site.site_header = "Reddit Admin"
admin.site.site_title = "Reddit Administration"

admin.site.unregister(Group)
