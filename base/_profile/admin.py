from django.contrib import admin
from . models import UserProfile
admin.site.register(UserProfile)

# from _profile.forms import GroupAdminForm
# from django.contrib.auth.models import Group
# admin.site.unregister(Group)
# @admin.register(Group)
# class GroupAdmin(admin.ModelAdmin):
#     form = GroupAdminForm